00449b04 xor edx, edx
00449b06 mov dl, byte ptr [esi + 0x12]
00449b09 add esp, 4
00449b0c neg edx
00449b0e push 0x5bdb9c
00449b13 lea ecx, [eax + edx*8]
00449b16 mov eax, dword ptr [esp + 0x54]
00449b1a xor edx, edx
00449b1c mov dword ptr [0x5b56d0], ecx
00449b22 mov dl, byte ptr [esi + 0x12]
00449b25 lea ecx, [eax + edx*8]
00449b28 mov edx, dword ptr [esp + 0x54]
00449b2c mov eax, dword ptr [esi + 0x14]
00449b2f push ecx
00449b30 push edx
00449b31 push eax
00449b32 call 0x401604
00449b37 mov edx, dword ptr [0x5b56d0]
00449b3d add esp, 0x10
00449b40 xor ecx, ecx
00449b42 mov cl, byte ptr [esi + 0x12]
00449b45 lea eax, [edx + ecx*8]
00449b48 mov dword ptr [0x5b56d0], eax
0045cfe8 movsx eax, cx
0045cfeb movsx ebx, di
0045cfee mov dword ptr [esp + 0x20], eax
0045cff2 mov eax, ebx
0045cff4 mov ecx, dword ptr [esp + 0xfc]
0045cffb mov dword ptr [esp + 0x74], ebx
0045cfff cdq 
0045d000 and edx, 3
0045d003 add eax, edx
0045d005 sar eax, 2
0045d008 movsx ebp, bp
0045d00b add ax, cx
0045d00e mov dword ptr [esp + 0x54], ebp
0045d012 mov word ptr [0x5bd744], ax
0045d018 mov eax, ebp
0045d01a movsx edi, word ptr [0x5bd754]
0045d021 cdq 
0045d022 and edx, 3
0045d025 mov dword ptr [esp + 0x70], edi
0045d029 add eax, edx
0045d02b sar eax, 2
0045d02e add ax, cx
0045d031 mov word ptr [0x5bd74c], ax
0045d037 mov eax, edi
0045d039 cdq 
0045d03a and edx, 3
0045d03d mov edi, dword ptr [esp + 0x68]
0045d041 add eax, edx
0045d043 sar eax, 2
0045d046 add ax, cx
0045d049 mov word ptr [0x5bd754], ax
0045d04f mov eax, dword ptr [esp + 0x20]
0045d053 cdq 
0045d054 and edx, 3
0045d057 add eax, edx
0045d059 sar eax, 2
0045d05c add ax, cx
0045d05f mov word ptr [0x5bd75c], ax
0045e69a movsx eax, word ptr [edi*4 + 0x573408]
0045e6a2 mov dword ptr [esp + 0x14], eax
0045e6a6 mov eax, dword ptr [esp + 0x6c]
0045e6aa fild dword ptr [esp + 0x14]
0045e6ae movsx ecx, word ptr [edi*4 + 0x57340a]
0045e6b6 fdivr qword ptr [0x4c00e0]
0045e6bc mov dword ptr [esp + 0x14], ecx
0045e6c0 sub eax, 0x60
0045e6c3 neg eax
0045e6c5 sbb eax, eax
0045e6c7 and al, 0x81
0045e6c9 add eax, 0xff
0045e6ce cmp ax, 0xff
0045e6d2 mov dword ptr [esp + 0x18], eax
0045e6d6 fstp dword ptr [esp + 0x48]
0045e6da fild dword ptr [esp + 0x14]
0045e6de fdivr qword ptr [0x4c00e0]
0045e6e4 fstp dword ptr [esp + 0x24]
0045e6e8 jne 0x45e852
0045e9a3 mov dword ptr [esp + 0x14], edx
0045e9a7 fild dword ptr [esp + 0x14]
0045e9ab fstp dword ptr [edi]
0045e9ad movsx ecx, word ptr [0x5bd742]
0045e9b4 mov dword ptr [esp + 0x14], ecx
0045e9b8 fild dword ptr [esp + 0x14]
0045e9bc fstp dword ptr [edi + 4]
0045e9bf movsx edx, word ptr [0x5bd744]
0045e9c6 mov dword ptr [esp + 0x14], edx
0045e9ca fild dword ptr [esp + 0x14]
0045e9ce fmul dword ptr [0x4c00e8]
0045e9d4 fstp dword ptr [edi + 8]
0045e9d7 fild dword ptr [0x76f9a0]
0045e9dd fdivr dword ptr [0x4c00ec]
0045e9e3 fstp dword ptr [edi + 0xc]
0045e9e6 mov cl, byte ptr [esi + 0xe]
0045e9e9 and ecx, 0xff
0045e9ef movsx edx, cx
0045e9f2 mov dword ptr [esp + 0x14], edx
0045e9f6 fild dword ptr [esp + 0x14]
0045e9fa fmul dword ptr [esp + 0x48]
0045e9fe fstp dword ptr [edi + 0x18]
0045ea01 mov al, byte ptr [esi + 0xf]
0045ea04 movsx eax, ax
