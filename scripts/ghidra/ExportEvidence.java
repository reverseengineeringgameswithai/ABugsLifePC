// Reviewable Ghidra evidence export: functions, call relationships, data references,
// strings, imports, and decompiler text. Run through scripts/ghidra-export.sh.
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.address.AddressIterator;
import ghidra.program.model.listing.Data;
import ghidra.program.model.listing.DataIterator;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import ghidra.program.model.symbol.ReferenceManager;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.util.Set;

public class ExportEvidence extends GhidraScript {
    private BufferedWriter out;

    private String q(Object value) {
        if (value == null) return "null";
        String s = value.toString().replace("\\", "\\\\").replace("\"", "\\\"")
            .replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t");
        StringBuilder b = new StringBuilder("\"");
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c < 0x20) b.append(String.format("\\u%04x", (int)c)); else b.append(c);
        }
        return b.append("\"").toString();
    }

    private void stringArray(Iterable<?> values) throws Exception {
        out.write("[");
        boolean first = true;
        for (Object value : values) {
            if (!first) out.write(",");
            out.write(q(value));
            first = false;
        }
        out.write("]");
    }

    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length != 1) throw new IllegalArgumentException("Expected output JSON path");
        out = new BufferedWriter(new FileWriter(args[0]));
        DecompInterface decompiler = new DecompInterface();
        decompiler.openProgram(currentProgram);
        ReferenceManager refs = currentProgram.getReferenceManager();

        out.write("{\"program\":{\"name\":" + q(currentProgram.getName()) +
            ",\"executable_sha256\":" + q(currentProgram.getExecutableSHA256()) +
            ",\"image_base\":" + q(currentProgram.getImageBase()) + "},");

        out.write("\"functions\":[");
        FunctionIterator functions = currentProgram.getFunctionManager().getFunctions(true);
        boolean firstFunction = true;
        while (functions.hasNext() && !monitor.isCancelled()) {
            Function function = functions.next();
            if (function.isExternal()) continue;
            if (!firstFunction) out.write(",");
            firstFunction = false;
            out.write("{\"address\":" + q(function.getEntryPoint()) +
                ",\"name\":" + q(function.getName()) +
                ",\"prototype\":" + q(function.getPrototypeString(false, false)) + ",");

            out.write("\"callers\":[");
            ReferenceIterator callers = refs.getReferencesTo(function.getEntryPoint());
            boolean first = true;
            while (callers.hasNext()) {
                Reference ref = callers.next();
                if (!ref.getReferenceType().isCall()) continue;
                if (!first) out.write(",");
                out.write(q(ref.getFromAddress()));
                first = false;
            }
            out.write("],\"callees\":");
            Set<Function> callees = function.getCalledFunctions(monitor);
            stringArray(callees.stream().map(f -> f.getEntryPoint().toString()).toList());

            out.write(",\"data_references\":[");
            first = true;
            AddressIterator addresses = function.getBody().getAddresses(true);
            while (addresses.hasNext()) {
                Address from = addresses.next();
                for (Reference ref : refs.getReferencesFrom(from)) {
                    if (!ref.getReferenceType().isData()) continue;
                    if (!first) out.write(",");
                    out.write("{\"from\":" + q(from) + ",\"to\":" + q(ref.getToAddress()) +
                        ",\"type\":" + q(ref.getReferenceType()) + "}");
                    first = false;
                }
            }
            DecompileResults result = decompiler.decompileFunction(function, 60, monitor);
            String code = result.decompileCompleted() && result.getDecompiledFunction() != null
                ? result.getDecompiledFunction().getC() : null;
            out.write("],\"decompiler\":" + q(code) + "}");
        }

        out.write("],\"strings\":[");
        DataIterator data = currentProgram.getListing().getDefinedData(true);
        boolean first = true;
        while (data.hasNext() && !monitor.isCancelled()) {
            Data item = data.next();
            if (!item.hasStringValue()) continue;
            if (!first) out.write(",");
            out.write("{\"address\":" + q(item.getAddress()) + ",\"value\":" + q(item.getValue()) + "}");
            first = false;
        }

        out.write("],\"imports\":[");
        functions = currentProgram.getFunctionManager().getFunctions(true);
        first = true;
        while (functions.hasNext()) {
            Function function = functions.next();
            if (!function.isExternal()) continue;
            if (!first) out.write(",");
            out.write("{\"name\":" + q(function.getName()) +
                ",\"library\":" + q(function.getExternalLocation() == null ? null :
                    function.getExternalLocation().getLibraryName()) + "}");
            first = false;
        }
        out.write("]}\n");
        out.close();
        decompiler.dispose();
        println("Exported reviewable evidence to " + args[0]);
    }
}
