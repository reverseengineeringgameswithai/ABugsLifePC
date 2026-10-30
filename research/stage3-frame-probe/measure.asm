bits 32
org 0x4bbc00
%include "scene-offsets.inc"
%define D 0xc00000
db 'MS3P'
dd 1, D, 192, 2048
dd frame_begin-0x400000, render_begin-0x400000, frame_end-0x400000
dd collect-0x400000, batch0-0x400000, batch1-0x400000
dd admit0-0x400000, admit1-0x400000

; Each entry restores integer registers and flags before replaying the exact
; displaced operation. APIs use their native stdcall ABI. No pacing changes.
%macro BASE 0
call %%pc
%%pc: pop ebx
sub ebx, %%pc-0x400000
%endmacro

frame_begin:
pushfd
pushad
BASE
cmp dword [ebx+0x461c84],1
jne .done
lea eax,[ebx+D]
cmp [ebx+0x1c5964],eax
jae .done
cmp dword [ebx+D+12],0
jne .initialized
lea eax,[ebx+kernel-0x400000]
push eax
call [ebx+0x464660] ; GetModuleHandleA
test eax,eax
jz .failed
mov esi,eax
lea eax,[ebx+qpc_name-0x400000]
push eax
push esi
call [ebx+0x464654] ; GetProcAddress
test eax,eax
jz .failed
mov [ebx+D+4],eax
lea eax,[ebx+qpf_name-0x400000]
push eax
push esi
call [ebx+0x464654]
test eax,eax
jz .failed
mov [ebx+D+8],eax
lea edx,[ebx+D+16]
push edx
call eax
test eax,eax
jz .failed
mov eax,[ebx+D+16]
or eax,[ebx+D+20]
jz .failed
mov dword [ebx+D+12],1
.initialized:
cmp dword [ebx+D+12],1
jne .done
cld
lea edi,[ebx+D+64]
xor eax,eax
mov ecx,12
rep stosd
mov [ebx+D+52],eax
mov [ebx+D+32],eax
mov [ebx+D+36],eax
lea eax,[ebx+D+56]
push eax
call [ebx+D+4]
test eax,eax
jz .failed
lea eax,[ebx+D+24]
push eax
call [ebx+D+4]
test eax,eax
jz .failed
mov eax,[ebx+D+24]
sub eax,[ebx+D+56]
mov [ebx+D+112],eax
mov dword [ebx+D+48],1
jmp .done
.failed:
mov dword [ebx+D+12],-1
mov dword [ebx+D+48],0
.done:
popad
popfd
call 0x401e79
jmp 0x40ffcf

render_begin:
pushfd
pushad
BASE
mov [ebx+0xed714],eax ; displaced native timeGetTime timestamp store
cmp dword [ebx+D+48],1
jne .done
lea eax,[ebx+D+32]
push eax
call [ebx+D+4]
test eax,eax
jnz .done
or dword [ebx+D+52],1
.done:
popad
popfd
jmp 0x405c0c

collect:
pushfd
pushad
BASE
cmp dword [ebx+D+48],1
jne .done
inc dword [ebx+D+68]
cmp eax,[ebx+D+64]
jbe .all_max
mov [ebx+D+64],eax
.all_max:
cmp eax,400
jbe .bounded
or dword [ebx+D+52],2
.bounded:
lea ecx,[ebx+0x19d910]
cmp ecx,[esp+36+0x50]
jne .done
inc dword [ebx+D+76]
cmp eax,[ebx+D+72]
jbe .done
mov [ebx+D+72],eax
.done:
popad
popfd
shl ebp,2
cmp eax,esi
jmp 0x4ab75b

%macro BATCH 3
%1:
pushfd
pushad
BASE
cmp dword [ebx+D+48],1
jne %%done
lea edi,[esp+36]
inc dword [ebx+D+80]
mov eax,[edi+16]
add [ebx+D+84],eax
cmp eax,[ebx+D+92]
jbe %%max_v
mov [ebx+D+92],eax
%%max_v:
cmp eax,500
jbe %%v_bound
or dword [ebx+D+52],4
%%v_bound:
mov eax,[edi+24]
add [ebx+D+88],eax
cmp eax,[ebx+D+104+%2*4]
jbe %%max_i
mov [ebx+D+104+%2*4],eax
%%max_i:
cmp eax,%3
jbe %%done
or dword [ebx+D+52],8
%%done:
popad
popfd
call [ebp+0x78]
test eax,eax
%if %2 == 0
jmp 0x40581b
%else
jmp 0x405990
%endif
%endmacro
BATCH batch0,0,1000
BATCH batch1,1,4800

%macro ADMIT 4
%1:
pushfd
pushad
BASE
cmp dword [ebx+D+48],1
jne %%done
inc dword [ebx+D+96]
mov eax,esi
sub eax,[ebx+0x1ba240]
cmp eax,SCENE160
jne %%next1
or dword [ebx+D+100],1
%%next1:
cmp eax,SCENE484
jne %%next2
or dword [ebx+D+100],2
%%next2:
cmp eax,SCENE485
jne %%next3
or dword [ebx+D+100],4
%%next3:
cmp eax,SCENE486
jne %%done
or dword [ebx+D+100],8
%%done:
popad
popfd
mov eax,[esp+%2]
mov edx,[esp+%3]
jmp %4
%endmacro
ADMIT admit0,0x1c,0x14,0x44d702
ADMIT admit1,0x20,0x18,0x44d71a

frame_end:
pushfd
pushad
BASE
cmp dword [ebx+D+48],1
jne .done
mov dword [ebx+D+48],0
lea eax,[ebx+D+40]
push eax
call [ebx+D+4]
test eax,eax
jnz .counter_ok
or dword [ebx+D+52],1
.counter_ok:
mov eax,[ebx+D]
and eax,2047
imul eax,192
lea edi,[ebx+D+0x100+eax]
mov ebp,edi
mov dword [edi],0 ; incomplete record until final sequence publication
mov eax,[esp+24] ; original ECX = native rendering elapsed milliseconds
mov [edi+4],eax
mov eax,[ebx+D+40]
mov edx,[ebx+D+44]
sub eax,[ebx+D+24]
sbb edx,[ebx+D+28]
mov [edi+8],eax
mov [edi+12],edx
mov eax,[ebx+D+40]
mov edx,[ebx+D+44]
sub eax,[ebx+D+32]
sbb edx,[ebx+D+36]
mov [edi+16],eax
mov [edi+20],edx
cld
add edi,24
lea esi,[ebx+D+24]
movsd
movsd
lea esi,[ebx+D+40]
movsd
movsd
mov eax,[ebx+0x461c84]
stosd
mov eax,[ebx+0x199af4]
stosd
lea esi,[ebx+0x19d910]
mov ecx,3
rep movsd
mov eax,[ebx+0x19d930]
stosd
lea esi,[ebx+0x1b58e0]
mov ecx,9
rep movsw
xor eax,eax
stosw
lea esi,[ebx+0x1bdb8c]
mov ecx,3
rep movsd
lea esi,[ebx+D+64]
mov ecx,12
rep movsd
mov eax,[ebx+D+52]
stosd
; Bounded native actor census: twenty48-byte moving records.
xor edx,edx
xor eax,eax
lea esi,[ebx+0x19d9c0]
mov ecx,20
.actors:
cmp word [esi],0
jle .actor_next
inc edx
movzx edi,word [esi]
cmp edi,31
ja .actor_next
bts eax,edi
.actor_next:
add esi,48
loop .actors
mov [ebp+148],edx
mov [ebp+152],eax
xor edx,edx
lea esi,[ebx+0x19b628]
mov ecx,64
.seeds:
cmp dword [esi],0
jle .seed_next
test word [esi+92],32
jz .seed_next
inc edx
.seed_next:
add esi,132
loop .seeds
mov [ebp+156],edx
mov eax,[ebx+0x3f3d68]
mov [ebp+160],eax
mov ax,[ebx+0x19d992]
mov [ebp+164],ax
mov al,[ebx+0x19d9b0]
mov [ebp+166],al
mov byte [ebp+167],0
mov eax,[ebx+0x1c5964]
mov [ebp+168],eax
mov eax,[ebx+0xed714]
mov [ebp+172],eax
mov ax,[ebx+0x19a5b0]
mov [ebp+176],ax
mov ax,[ebx+0x19d9a4]
mov [ebp+178],ax
movzx eax,word [ebx+0x19f7f0]
mov edx,[ebx+0x1c2410]
shl edx,16
or eax,edx
mov [ebp+180],eax
mov eax,[ebx+D+112]
mov [ebp+184],eax
mov eax,[ebx+D]
inc eax
mov [ebp+188],eax
mov [ebp],eax
mov [ebx+D],eax
.done:
popad
popfd
xor edx,edx
inc ecx
div ecx
jmp 0x405b68

kernel: db 'kernel32.dll',0
qpc_name: db 'QueryPerformanceCounter',0
qpf_name: db 'QueryPerformanceFrequency',0
