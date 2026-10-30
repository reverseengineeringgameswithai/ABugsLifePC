0045a7f0: 81ece0000000 sub esp, 0xe0
0045a7f6: a1d0565b00 mov eax, dword ptr [0x5b56d0]
0045a7fb: 53 push ebx
0045a7fc: 55 push ebp
0045a7fd: 56 push esi
0045a7fe: 57 push edi
0045a7ff: 8bbc24f4000000 mov edi, dword ptr [esp + 0xf4]
0045a806: 8d0c8500feffff lea ecx, [eax*4 - 0x200]
0045a80d: 85ff test edi, edi
0045a80f: 894c2450 mov dword ptr [esp + 0x50], ecx
0045a813: 0f844d5a0000 je 0x460266
0045a819: b818d85b00 mov eax, 0x5bd818
0045a81e: 8d7704 lea esi, [edi + 4]
0045a821: 2d44440000 sub eax, 0x4444
0045a826: 8974244c mov dword ptr [esp + 0x4c], esi
0045a82a: 89442464 mov dword ptr [esp + 0x64], eax
0045a82e: 8b07 mov eax, dword ptr [edi]
0045a830: 85c0 test eax, eax
0045a832: 7d63 jge 0x45a897
0045a834: f7d8 neg eax
0045a836: 8907 mov dword ptr [edi], eax
0045a838: 8bc8 mov ecx, eax
0045a83a: 8d1440 lea edx, [eax + eax*2]
0045a83d: 83e101 and ecx, 1
0045a840: 8d2c96 lea ebp, [esi + edx*4]
0045a843: 8d1440 lea edx, [eax + eax*2]
0045a846: 83c003 add eax, 3
0045a849: 83c502 add ebp, 2
0045a84c: 2bd1 sub edx, ecx
0045a84e: 896c2428 mov dword ptr [esp + 0x28], ebp
0045a852: 8d0440 lea eax, [eax + eax*2]
0045a855: c1e002 shl eax, 2
0045a858: 85c0 test eax, eax
0045a85a: 8d745502 lea esi, [ebp + edx*2 + 2]
0045a85e: 7e27 jle 0x45a887
0045a860: 8d502f lea edx, [eax + 0x2f]
0045a863: b8abaaaaaa mov eax, 0xaaaaaaab
0045a868: f7e2 mul edx
0045a86a: b918595b00 mov ecx, 0x5b5918
0045a86f: c1ea05 shr edx, 5
0045a872: c641e800 mov byte ptr [ecx - 0x18], 0
0045a876: c641f400 mov byte ptr [ecx - 0xc], 0
0045a87a: c60100 mov byte ptr [ecx], 0
0045a87d: c6410c00 mov byte ptr [ecx + 0xc], 0
0045a881: 83c130 add ecx, 0x30
0045a884: 4a dec edx
0045a885: 75eb jne 0x45a872
0045a887: 8b07 mov eax, dword ptr [edi]
0045a889: c744243c00595b00 mov dword ptr [esp + 0x3c], 0x5b5900
0045a891: f7d8 neg eax
0045a893: 8907 mov dword ptr [edi], eax
0045a895: eb0a jmp 0x45a8a1
0045a897: 8b6c2428 mov ebp, dword ptr [esp + 0x28]
0045a89b: 8d0c40 lea ecx, [eax + eax*2]
0045a89e: 8d348e lea esi, [esi + ecx*4]
0045a8a1: 85f6 test esi, esi
0045a8a3: 0f84bd590000 je 0x460266
0045a8a9: 8b9c2400010000 mov ebx, dword ptr [esp + 0x100]
0045a8b0: 66833eff cmp word ptr [esi], -1
0045a8b4: 0f84ac590000 je 0x460266
0045a8ba: 66c70544d74e00ff00 mov word ptr [0x4ed744], 0xff
0045a8c3: 0fbf06 movsx eax, word ptr [esi]
0045a8c6: 8bd0 mov edx, eax
0045a8c8: 83e21f and edx, 0x1f
0045a8cb: 8bca mov ecx, edx
0045a8cd: 8954247c mov dword ptr [esp + 0x7c], edx
0045a8d1: 83e101 and ecx, 1
0045a8d4: 83e900 sub ecx, 0
0045a8d7: 0f84bf1e0000 je 0x45c79c
0045a8dd: 49 dec ecx
0045a8de: 0f8582590000 jne 0x460266
0045a8e4: 8bc8 mov ecx, eax
0045a8e6: 83c604 add esi, 4
0045a8e9: c1f808 sar eax, 8
0045a8ec: 83e01f and eax, 0x1f
0045a8ef: 83e160 and ecx, 0x60
0045a8f2: 89442468 mov dword ptr [esp + 0x68], eax
0045a8f6: 894c246c mov dword ptr [esp + 0x6c], ecx
0045a8fa: 0fbf46fe movsx eax, word ptr [esi - 2]
0045a8fe: 85c0 test eax, eax
0045a900: 89442478 mov dword ptr [esp + 0x78], eax
0045a904: 0f8e54590000 jle 0x46025e
0045a90a: 4a dec edx
0045a90b: 89542414 mov dword ptr [esp + 0x14], edx
0045a90f: 8b442414 mov eax, dword ptr [esp + 0x14]
0045a913: 83f80a cmp eax, 0xa
0045a916: 772e ja 0x45a946
0045a918: 33d2 xor edx, edx
0045a91a: 8a9054104600 mov dl, byte ptr [eax + 0x461054]
