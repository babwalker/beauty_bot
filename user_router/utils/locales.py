ru_start_message = """
👋 Добро пожаловать в консультационный бот от онлайн-косметолога Академии BWA!

🌿 Здесь вы можете получить персональные рекомендации по уходу за кожей — без визита в салон!

📸 Просто загрузите фото лица, укажите ваш тип кожи и ответьте на несколько вопросов —  
а мы подготовим для вас индивидуальный план ухода: утром, вечером, и на неделю вперёд.

💡 Наши рекомендации:
— Без рекламы  
— Основаны на вашем типе кожи  
— От сертифицированных специалистов  

🎥 Посмотрите короткое видео, как работает онлайн-анализ кожи:  
[🔗 Видео 1 — Как проходит skin-анализ]

🎥 А также видео с отзывом клиента:  
[🔗 Видео 2 — Отзыв студентки об онлайн-косметологе]

👇 Что вас интересует?
1️⃣ Пройти skin-анализ  
2️⃣ Узнать больше об уходе за кожей  
3️⃣ Получить консультацию от косметолога  
4️⃣ Задать вопрос
"""

en_start_message = """
👋 Welcome to the consultation bot from BWA Academy's online cosmetologist!

🌿 Here you can get personalized skincare recommendations - without a salon visit!

📸 Just upload a photo of your face, indicate your skin type and answer a few questions - and we'll prepare a personalized consultation for you.  
and we'll prepare a personalized care plan for you: morning, evening, and for the week ahead.

💡 Our recommendations:
- Ad-free  
- Based on your skin type  
- From certified professionals  

🎥 Watch a short video on how online skin analysis works:  
[🔗 Video 1 - How Skin Analysis Works]

🎥 And also a client testimonial video:  
[🔗 Video 2 - Student's Review of Online Cosmetologist].

👇 What are you interested in?
1️⃣ Get a skin analysis  
2️⃣ Learn more about skin care  
3️⃣ Get a consultation from a cosmetologist  
4️⃣ Ask a question
"""

de_start_message = """
👋 Willkommen beim Beratungsbot der Online-Kosmetikerin der BWA-Akademie!

🌿 Hier bekommst du persönliche Pflegeempfehlungen - ganz ohne Salonbesuch!

📸 Laden Sie einfach ein Foto Ihres Gesichts hoch, geben Sie Ihren Hauttyp an und beantworten Sie ein paar Fragen - und schon erstellen wir eine individuelle Beratung für Sie.  
und wir erstellen einen persönlichen Pflegeplan für Sie: morgens, abends und für die kommende Woche.

💡 Unsere Empfehlungen:
- Werbefrei  
- Basierend auf Ihrem Hauttyp  
- Von zertifizierten Fachleuten  

🎥 Sehen Sie in einem kurzen Video, wie die Online-Hautanalyse funktioniert:  
[🔗 Video 1 - Wie die Hautanalyse funktioniert]

🎥 Und auch ein Video mit Kundenaussagen:  
[🔗 Video 2 - Student's Review of Online Cosmetologist].

👇 Woran sind Sie interessiert?
1️⃣ Eine Hautanalyse erhalten  
2️⃣ Mehr über Hautpflege erfahren  
3️⃣ Lassen Sie sich von einer Kosmetikerin beraten  
4️⃣ Eine Frage stellen
"""

translations = {
    "ru": {
        "back_button": "⬅️ Назад",
        "other_button": "Другое",
        "done_button": "Готово",
        "start": ru_start_message,
        "start_skin_analys": "Как тебя зовут?",
        "name_error": "Имя должно содержать минимум 2 символа. Попробуйте еще раз.",
        "country_question": "В какой стране ты живешь?",
        "email_question": "Укажи свой email:",
        "email_error": "Это не похоже на email. Введите корректный email.",
        "age_question": "Сколько тебе лет?",
        "gender_question": "Укажи свой пол:",
        "skin_type_question": "Как бы ты описал(а) свою кожу?",
        "skin_problems_question": "Какие проблемы вас беспокоят? (Максимум 3)",
        "max_amount_warning": "Можно выбрать не более 3 вариантов",
        "min_amount_warning": "Выберите хотя бы один вариант",
        "skin_features_question": "Какие у вас особенности кожи?",
        "lifestyle_question": "Какой у вас образ жизни? (Максимум 3)",
        "water_question": "Сколько воды вы выпиваете в день?",
        "products_question": "Какие косметические продукты вы используете ежедневно?",
        "procedures_question": "Как часто вы делаете профессиональные косметологические процедуры?",
        "budget_question": "Какой бюджет на уход вам комфортен?",
        "composition_question": "Есть ли у вас пожелания по составу косметики?",
        "upload_full_face_photo": (
            "Загрузите фото лица для анализа - 📌 Важно: "
            "Фото должно быть сделано без макияжа, при хорошем освещении, анфас."
        ),
        "upload_right_profile_photo": (
            "Загрузите фото лица для анализа - 📌 Важно: "
            "Фото должно быть сделано без макияжа, при хорошем освещении, профиль справа"
        ),
        "upload_left_profile_photo": (
            "Загрузите фото лица для анализа - 📌 Важно: "
            "Фото должно быть сделано без макияжа, при хорошем освещении, профиль слева."
        ),
        "no_face_error": "Отправьте изображение с лицом",
        "other_skin_problems": "Укажите другие проблемы кожи:",
        "other_daily_products": "Укажите другие используемые продукты:",
        "procedures_frequency_question": "Как часто вы делаете профессиональные косметологические процедуры?",
        "processing_photo": "Анализ фото...",
        "full_face": "Загружено",
        "no_face_error_left": "Отправьте изображение с лицом (профиль слева)",
        "thanks_message": (
            "Спасибо за ответы! На основе ваших предпочтений мы подобрали оптимальную программу ухода"
        ),
        "report": "Отчет",
        "email_validation": "Введите корректный email",
        "other_message": "Выберите подходящий для вас вариант..."
    },
    "en": {
        "back_button": "⬅️ Back",
        "other_button": "Other",
        "done_button": "Done",
        "start": en_start_message,
        "start_skin_analys": "What's your name?",
        "name_error": "Name must be at least 2 characters long. Please try again.",
        "country_question": "In which country do you live?",
        "email_question": "Enter your email:",
        "email_error": "This doesn't look like an email. Please enter a valid one.",
        "age_question": "How old are you?",
        "gender_question": "What is your gender?",
        "skin_type_question": "How would you describe your skin?",
        "skin_problems_question": "What skin concerns do you have? (Maximum 3)",
        "max_amount_warning": "You can select up to 3 options only",
        "min_amount_warning": "Please select at least one option",
        "skin_features_question": "Do you have any skin features?",
        "lifestyle_question": "What is your lifestyle like? (Maximum 3)",
        "water_question": "How much water do you drink per day?",
        "products_question": "What skincare products do you use daily?",
        "procedures_question": "How often do you get professional cosmetic treatments?",
        "budget_question": "What is your comfortable skincare budget?",
        "composition_question": "Do you have any preferences regarding cosmetic ingredients?",
        "upload_full_face_photo": (
            "Upload a photo of your face for analysis - 📌 Important: "
            "The photo should be taken without makeup, with good lighting, and face forward."
        ),
        "upload_right_profile_photo": (
            "Upload a profile photo for analysis - 📌 Important: "
            "The photo should be taken without makeup, with good lighting, right side profile."
        ),
        "no_face_error": "Please send an image containing a face",
        "gender_question": "Specify your gender:",
        "other_skin_problems": "Specify other skin problems:",
        "other_daily_products": "Specify other products you use:",
        "procedures_frequency_question": "How often do you undergo professional cosmetic procedures?",
        "processing_photo": "Analyzing the photo...",
        "full_face": "Uploaded",
        "upload_left_profile_photo": (
            "Upload a face photo for analysis - 📌 Important: "
            "The photo should be without makeup, with good lighting, left profile view."
        ),
        "no_face_error_left": "Please send an image with a face (left profile)",
        "thanks_message": (
            "Thank you for your answers! Based on your preferences, we've selected the optimal care program"
        ),
        "report": "Report",
        "email_validation": "Enter a valid email",
        "other_message": "Choose the option that is right for you..."
    },
    "de": {
        "back_button": "⬅️ Zurück",
        "other_button": "Andere",
        "done_button": "Fertig",
        "start": de_start_message,
        "start_skin_analys": "Wie ist Ihr Name?",
        "name_error": "Der Name muss mindestens 2 Zeichen lang sein. Bitte versuche es erneut.",
        "country_question": "In welchem Land lebst du?",
        "email_question": "Gib deine E-Mail-Adresse an:",
        "email_error": "Das sieht nicht wie eine E-Mail aus. Bitte eine gültige eingeben.",
        "age_question": "Wie alt bist du?",
        "gender_question": "Was ist dein Geschlecht?",
        "skin_type_question": "Wie würdest du deine Haut beschreiben?",
        "skin_problems_question": "Welche Hautprobleme hast du? (Maximal 3)",
        "max_amount_warning": "Du kannst nur bis zu 3 Optionen auswählen",
        "min_amount_warning": "Bitte wähle mindestens eine Option aus",
        "skin_features_question": "Gibt es Besonderheiten deiner Haut?",
        "lifestyle_question": "Wie ist dein Lebensstil? (Maximal 3)",
        "water_question": "Wie viel Wasser trinkst du täglich?",
        "products_question": "Welche Hautpflegeprodukte benutzt du täglich?",
        "procedures_question": "Wie oft lässt du professionelle kosmetische Behandlungen durchführen?",
        "budget_question": "Welches Pflegebudget ist für dich angenehm?",
        "composition_question": "Hast du Wünsche bezüglich der Inhaltsstoffe?",
        "upload_full_face_photo": (
            "Lade ein Foto deines Gesichts zur Analyse hoch – 📌 Wichtig: "
            "Das Foto sollte ohne Make-up, bei guter Beleuchtung und frontal aufgenommen werden."
        ),
        "upload_right_profile_photo": (
            "Lade ein Profilfoto zur Analyse hoch – 📌 Wichtig: "
            "Das Foto sollte ohne Make-up, bei guter Beleuchtung und im rechten Profil aufgenommen werden."
        ),
        "no_face_error": "Bitte sende ein Bild mit einem Gesicht",
        "gender_question": "Gib dein Geschlecht an:",
        "other_skin_problems": "Gib weitere Hautprobleme an:",
        "other_daily_products": "Gib andere verwendete Produkte an:",
        "procedures_frequency_question": "Wie oft lässt du professionelle kosmetische Behandlungen durchführen?",
        "processing_photo": "Analyse des Fotos...",
        "full_face": "Hochgeladen",
        "upload_left_profile_photo": (
            "Laden Sie ein Gesichtsfoto zur Analyse hoch - 📌 Wichtig: "
            "Das Foto sollte ohne Make-up, bei guter Beleuchtung, im linken Profil aufgenommen sein."
        ),
        "no_face_error_left": "Bitte senden Sie ein Bild mit einem Gesicht (linkes Profil)",
        "thanks_message": (
            "Vielen Dank für Ihre Antworten! Basierend auf Ihren Präferenzen haben wir das optimale Pflegeprogramm ausgewählt"
        ),
        "report": "Bericht",
        "email_validation": "Geben Sie eine gültige E-Mail ein",
        "other_message": "Wählen Sie die Option, die für Sie geeignet ist..."
    }
}

fields_translations = {
    "ru": {
        "name": "Имя",
        "country": "Страна проживания",
        "email": "Email",
        "age": "Возраст",
        "gender": "Пол",
        "skin_type": "Тип кожи",
        "skin_problems": "Проблемы с кожей",
        "skin_features": "Особенности кожи",
        "lifestyles": "Образ жизни",
        "water_intake": "Потребление воды в день",
        "daily_products": "Ежедневные косметические продукты",
        "procedures_frequency": "Частота профиссиональных косметических процедур",
        "budget": "Бюджет",
        "composition_prefs": "Пожелания по составу косметики",
        "full_face": "Фотография анфас",
        "right_side_face": "Фотография профиля справа",
        "left_side_face": "Фотография профиля слева"
    },
    "en": {
        "name": "Name",
        "country": "Country of residence",
        "email": "Email",
        "age": "Age",
        "gender": "Gender",
        "skin_type": "Skin type",
        "skin_problems": "Skin problems",
        "skin_features": "Особенности кожи",
        "lifestyles": "Lifestyles",
        "water_intake": "Water intake per day",
        "daily_products": "Daily cosmetic products",
        "procedures_frequency": "Frequency of professional procedures",
        "budget": "Budget",
        "composition_prefs": "Cosmetic composition preferences",
        "full_face": "Full face photo",
        "right_side_face": "Right profile photo",
        "left_side_face": "Left profile photo"
    },
    "de": {
        "name": "Name",
        "country": "Wohnsitzland",
        "email": "E-Mail",
        "age": "Alter",
        "gender": "Geschlecht",
        "skin_type": "Hauttyp",
        "skin_problems": "Hautprobleme",
        "skin_features": "Merkmale der Haut",
        "lifestyles": "Lebensstile",
        "water_intake": "Wasseraufnahme pro Tag",
        "daily_products": "Tägliche Kosmetikprodukte",
        "procedures_frequency": "Häufigkeit professioneller Behandlungen",
        "budget": "Budget",
        "composition_prefs": "Präferenzen für Kosmetikzusammensetzung",
        "full_face": "Porträtaufnahme",
        "right_side_face": "Rechtsprofilfoto",
        "left_side_face": "Linksprofilfoto"
    }
}