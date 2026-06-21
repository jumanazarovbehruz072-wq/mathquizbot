# questions.py
# Bu yerga o'zingiz xohlagancha savol qo'shishingiz yoki o'chirishingiz mumkin.
# Har bir savol quyidagi formatda bo'lishi kerak:
#
# {
#     "question": "Savol matni",
#     "options": ["A javob", "B javob", "C javob", "D javob"],
#     "correct": 0,  # to'g'ri javobning options ichidagi indeksi (0 dan boshlanadi)
# }
#
# "correct" - options ro'yxatidagi to'g'ri javobning o'rni (0 = birinchi, 1 = ikkinchi, ...)

QUESTIONS = [
    {
        "question": "12 + 25 = ?",
        "options": ["35", "37", "47", "27"],
        "correct": 1,
    },
    {
        "question": "9 × 7 = ?",
        "options": ["56", "63", "72", "54"],
        "correct": 1,
    },
    {
        "question": "144 ning kvadrat ildizi nechaga teng?",
        "options": ["11", "12", "13", "14"],
        "correct": 1,
    },
    {
        "question": "2x + 5 = 15 tenglamada x nechaga teng?",
        "options": ["3", "4", "5", "10"],
        "correct": 1,
    },
    {
        "question": "Doiraning yuzi qaysi formula bilan topiladi?",
        "options": ["2πr", "πr²", "πd", "4πr²"],
        "correct": 1,
    },
    {
        "question": "100 ning 25% i nechaga teng?",
        "options": ["20", "25", "30", "15"],
        "correct": 1,
    },
    {
        "question": "Uchburchak ichki burchaklari yig'indisi necha gradus?",
        "options": ["90°", "180°", "270°", "360°"],
        "correct": 1,
    },
    {
        "question": "(-3) × (-4) = ?",
        "options": ["-12", "12", "-7", "7"],
        "correct": 1,
    },
    {
        "question": "Sonlar ketma-ketligi: 2, 4, 8, 16, ... keyingi son?",
        "options": ["20", "24", "32", "18"],
        "correct": 2,
    },
    {
        "question": "5! (5 faktorial) nechaga teng?",
        "options": ["20", "60", "120", "100"],
        "correct": 2,
    },
    {
        "question": "Agar a = 3, b = 4 bo'lsa, a² + b² = ?",
        "options": ["7", "12", "25", "49"],
        "correct": 2,
    },
    {
        "question": "3/4 kasrni o'nlik kasrga aylantiring",
        "options": ["0.25", "0.5", "0.75", "0.34"],
        "correct": 2,
    },
    {
        "question": "To'g'ri to'rtburchakning perimetri qanday topiladi?",
        "options": ["a × b", "2(a+b)", "a + b", "a² + b²"],
        "correct": 1,
    },
    {
        "question": "1000 ning 10% i nechaga teng?",
        "options": ["10", "100", "1", "1000"],
        "correct": 1,
    },
    {
        "question": "Eng kichik tub son qaysi?",
        "options": ["0", "1", "2", "3"],
        "correct": 2,
    },
]
