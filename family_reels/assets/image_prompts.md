# AI rasm/video promptlari (9:16, 1080x1920 yoki kattaroq)

Fayllarni `assets/images/s1.jpg … s6.jpg` nomi bilan saqlang (png ham bo‘ladi), keyin `./render.sh` ni ishga tushiring.
Umumiy uslub: warm natural light, cinematic, shallow depth of field, modest family clothing, no text, no watermark, vertical 9:16, upper-middle area of the frame kept uncluttered (matn uchun joy).

| Fayl | Kadr | Prompt |
|---|---|---|
| s1.jpg | HOOK | Cinematic vertical photo, a Muslim husband and wife sitting at a sunlit kitchen table in the morning, looking at each other with respect and a gentle smile, warm golden light through a window, tea cups, cozy modern home, shallow depth of field, 9:16, no text |
| s2.jpg | Hadis haqida | Warm vertical photo, husband gently handing his wife a cup of tea in a bright living room, calm respectful expressions, soft window light, natural candid style, 9:16, no text |
| s3.jpg | Kundalik hayot | Vertical lifestyle photo of a family at home: father kneeling to talk kindly with his young daughter, mother smiling nearby, couple setting the table together, warm evening light, authentic and tender, 9:16, no text |
| s4.jpg | Hadis fon | Soft, calm vertical background: out-of-focus warm home interior with window light, gentle bokeh, muted golden-brown tones, very low contrast and uncluttered (hadis kartasi ustiga chiqadi), 9:16, no people or distant silhouettes only |
| s5.jpg | Amaliy xulosa | Vertical photo, mother hugging her child while the father smiles beside them, couple holding hands on a sofa, warm sunset light, loving atmosphere, 9:16, no text |
| s6.jpg | Yakun | Vertical cinematic photo, happy family of four walking together in a park at golden hour, seen from behind or in soft side view, parents holding children’s hands, warm glow, 9:16, no text |

Eslatma: ayollar uchun hijob/odob talab qilinsa, promptga "modest clothing, hijab" qo‘shing.
Video material (mp4) ishlatmoqchi bo‘lsangiz, `scripts/render_scenes.py` da fon kirishini video qabul qiladigan qilib o‘zgartirish kerak (hozir faqat rasm).
