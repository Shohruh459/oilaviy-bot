# AI rasm promptlari (9:16 vertical) — bir xil oila, bir xil kino uslubi

Fayllar: `assets/images/s1.jpg, s2.jpg, s3.jpg, s4.jpg, s5.jpg, s6.jpg` (png ham bo‘ladi). Kamida 1080x1920, ideal 1620x2880.

## Ishlash tartibi (personajlar bir xil chiqishi uchun)
1. Avval **S1** ni generatsiya qiling. Eng yaxshi variantni tanlang.
2. S2, S3, S5, S6 ni generatsiya qilganda S1 ni **reference image** sifatida bering (Higgsfield "reference", Midjourney `--cref`, Flux/Kontext reference va h.k.) va "same man, same woman, same children as the reference" talabini saqlang.
3. S4 da odam yo‘q — u hadis kartasi uchun sokin fon.

## UMUMIY BLOKLAR (har promptga qo‘shiladi — o‘zgartirmang)

**CHARACTER BLOCK** (bir xil oila):
`Same Uzbek family in every image: husband, about 33, short dark brown hair, neatly trimmed short beard, warm brown eyes, calm kind face, wearing a plain beige shirt under a navy knit cardigan; wife, about 30, Central Asian features, soft natural face, wearing a dusty-rose hijab fully covering her hair and neck and a long loose modest cream dress with sleeves to the wrists; daughter, about 6, dark hair in two braids, light green modest dress; son, about 3, short dark hair, cream knit sweater. Natural, realistic faces and skin texture, subtle genuine expressions.`

**STYLE BLOCK** (bir xil uslub):
`Photorealistic cinematic photography, shot on 35mm lens, shallow depth of field, soft warm golden natural light, gentle film grain, muted warm color grade (honey, cream, soft brown), realistic skin, modest and respectful atmosphere, vertical 9:16, no text, no letters, no watermark, no logo.`

**SETTING BLOCK** (bir xil makon):
`Warm modern Uzbek home: light wooden furniture, a suzani-patterned cushion, ceramic teapot and small tea bowls (piyola), soft curtains, window light.`

**Kompozitsiya qoidasi:** odamlar kadrning pastki 55% ida; yuqori-o‘rta qismi (taxminan 15%–60%) toza va sokin bo‘lsin — u yerga keyin matn chiqadi.

---

## S1 — Hook (er-xotin bir-biriga hurmat bilan qaraydi)
```
[CHARACTER BLOCK: husband and wife only] [SETTING BLOCK] [STYLE BLOCK]
Morning scene. The husband and wife sit across from each other at a wooden kitchen table, looking at each other with warm respect and a gentle small smile, a teapot and two tea bowls between them. They keep a modest respectful distance, no physical contact. Soft sunlight from a window on the side. Medium shot, couple placed in the lower half of the frame, upper half is calm blurred wall and window light with empty space.
```

## S2 — Rasululloh ﷺ oilada yaxshi muomala (choy uzatish)
```
[CHARACTER BLOCK: husband and wife only] [SETTING BLOCK] [STYLE BLOCK]
The husband gently hands his wife a tea bowl with both hands, a respectful and caring gesture; the wife receives it with a soft grateful smile. Bright calm living room, warm window light. Medium shot, subjects in the lower half of the frame, upper half is soft out-of-focus wall and curtains with empty space.
```

## S3 — Kundalik hayot (ota–farzand, ona mehri, o‘zaro yordam)
```
[CHARACTER BLOCK: husband, wife, daughter, son] [SETTING BLOCK] [STYLE BLOCK]
Warm evening in the family home. The husband kneels to the daughter's eye level and talks to her kindly, listening with attention; in the background the wife smiles while setting the table, the little son sits nearby. Authentic, tender, candid documentary feel. Subjects in the lower 60% of the frame, upper area soft and uncluttered.
```

## S4 — Hadis kartasi uchun sokin fon (ODAM YO‘Q)
```
Serene minimalist background for a quote card, no people, no figures. Very soft out-of-focus warm interior with a window light glow, subtle abstract Islamic geometric (girih) pattern faintly visible in deep honey-brown and cream tones, low contrast, large calm empty center, gentle vignette, elegant and peaceful. Vertical 9:16, no text, no letters, no calligraphy, no watermark, no logo.
```
(Hadis matnini generatorga BERMANG — arabcha va o‘zbekcha matn HTML/CSS kartada chiqadi.)

## S5 — Amaliy xulosa (mehr, quchoq, oila)
```
[CHARACTER BLOCK: all four] [SETTING BLOCK] [STYLE BLOCK]
Loving family moment on a sofa: the wife hugs the little daughter, the husband sits beside them with a gentle smile, the small son leans on his father's lap. Modest, respectful posture between husband and wife, warm sunset light through the window. Subjects in the lower 60% of the frame, upper area soft and uncluttered.
```

## S6 — Yakun (baxtli oila birga yuradi)
```
[CHARACTER BLOCK: all four] [STYLE BLOCK]
Golden hour in a quiet park with autumn trees. The family walks together on a path, seen from a soft three-quarter back view, parents holding the children's hands, relaxed and happy; faces soft and natural where visible. Warm sunlight glow, gentle bokeh. Family in the lower half of the frame, upper half is glowing sky and out-of-focus trees with empty space.
```

---

## NEGATIVE PROMPT (barcha rasmlar uchun)
```
bad hands, extra fingers, distorted face, duplicate people, deformed anatomy, text, watermark, logo, blurry, low quality, unnatural skin, exaggerated expressions
```
(Qo‘shimcha tavsiya: `revealing clothing, uncovered hair on the wife, close romantic contact, uncanny face, plastic skin, extra limbs, different people between shots`.)
