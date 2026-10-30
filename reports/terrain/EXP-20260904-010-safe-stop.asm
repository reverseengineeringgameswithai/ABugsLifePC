004017cb jmp 0x405ad0
00405b49 mov edi, dword ptr [0x864884]
00405b4f call edi
00405b51 sub eax, dword ptr [0x4ed714]
00405b57 cdq
00405b58 mov ecx, eax
00405b5a mov eax, dword ptr [0x4f0678]
00405b5f xor ecx, edx
00405b61 sub ecx, edx
00405b63 xor edx, edx
00405b65 inc ecx
00405b66 div ecx
00405b68 cmp esi, -1
00405b6b mov dword ptr [0x4ed6f8], eax
00405b70 je 0x405b93
00405b72 call edi
00405b74 sub eax, dword ptr [0x4ed714]
00405b7a cdq
00405b7b mov ecx, eax
00405b7d mov eax, 0x3e8
00405b82 xor ecx, edx
00405b84 sub ecx, edx
00405b86 cdq
00405b87 inc ecx
00405b88 idiv ecx
00405b8a cmp eax, esi
00405b8c mov dword ptr [0x4ed6f8], eax
00405b91 jg 0x405b72
00405b93 pop edi
00405b94 pop esi
00405b95 mov ax, 1
00405b99 pop ebx
00405b9a ret
0044dbee call 0x4017cb
0044dbf3 pop edi
0044dbf4 pop esi
0044dbf5 pop ebp
0044dbf6 pop ebx
0044dbf7 add esp, 0x38
0044dbfa ret
