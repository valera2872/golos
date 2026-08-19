export const locales = ['en', 'ru', 'es', 'de', 'fr', 'tr'] as const;
export type Locale = (typeof locales)[number];

export const localeMeta: Record<Locale, { label: string; native: string; path: string }> = {
  en: { label: 'English', native: 'EN', path: '/' },
  ru: { label: 'Русский', native: 'RU', path: '/ru/' },
  es: { label: 'Español', native: 'ES', path: '/es/' },
  de: { label: 'Deutsch', native: 'DE', path: '/de/' },
  fr: { label: 'Français', native: 'FR', path: '/fr/' },
  tr: { label: 'Türkçe', native: 'TR', path: '/tr/' },
};

export const homeAlternates = locales.map((lang) => ({ lang, href: localeMeta[lang].path }));

export const homePath = (locale: Locale) => localeMeta[locale].path;

export type SiteCopy = {
  metaTitle: string;
  metaDescription: string;
  skip: string;
  nav: { product: string; how: string; morning: string; learn: string; app: string; language: string };
  hero: { eyebrow: string; title: string; lead: string; primary: string; secondary: string; note: string };
  proof: { title: string; text: string }[];
  flow: { eyebrow: string; title: string; lead: string; steps: { title: string; text: string }[] };
  capture: { eyebrow: string; title: string; lead: string; bullets: string[]; cta: string };
  morning: { eyebrow: string; title: string; lead: string; bullets: string[] };
  signs: { eyebrow: string; title: string; lead: string; bullets: string[] };
  beforeSleep: { eyebrow: string; title: string; lead: string; bullets: string[] };
  privacy: { eyebrow: string; title: string; lead: string };
  final: { eyebrow: string; title: string; lead: string; cta: string };
  footer: { tagline: string; product: string; learn: string; legal: string; privacy: string; terms: string; global: string };
  phone: {
    nightTitle: string; waiting: string; heard: string; recording: string; original: string;
    morningTitle: string; morningSub: string; dreamOne: string; dreamTwo: string; review: string;
    signsTitle: string; recurring: string; signOne: string; signTwo: string; signThree: string;
    sleepTitle: string; practice: string; story: string; sound: string; ready: string;
  };
};

export const copy: Record<Locale, SiteCopy> = {
  en: {
    metaTitle: 'Somnori — Capture Dreams Before They Disappear',
    metaDescription: 'Somnori is an Android-first nighttime dream journal built for hands-free capture, morning review and a personal dream history.',
    skip: 'Skip to content',
    nav: { product: 'Product', how: 'How it works', morning: 'Morning', learn: 'Learn', app: 'Android app', language: 'Language' },
    hero: {
      eyebrow: 'A dream can fade in seconds',
      title: 'Capture the dream. Stay half asleep.',
      lead: 'Wake from a dream, say your Somnori phrase, tell it while your eyes are still closed — then go back to sleep.',
      primary: 'See the night flow',
      secondary: 'Explore the dream journal',
      note: 'Android-first. Public release is being prepared.',
    },
    proof: [
      { title: 'No unlocking', text: 'Designed for the moment you do not want to fully wake up.' },
      { title: 'No typing', text: 'Speak before the fragments disappear.' },
      { title: 'Original audio', text: 'Keep the voice, not only a cleaned-up text.' },
      { title: 'Morning review', text: 'Return to the whole night when you are awake.' },
    ],
    flow: {
      eyebrow: 'Built around 3AM',
      title: 'Less friction between waking and remembering',
      lead: 'Somnori is not trying to replace your phone assistant. It is built for one fragile nighttime moment: catching a dream before the memory breaks apart.',
      steps: [
        { title: 'Wake', text: 'A scene, a voice or a feeling is still there.' },
        { title: 'Say Somnori', text: 'Start the night assistant without navigating the phone.' },
        { title: 'Tell the dream', text: 'Speak naturally. Somnori keeps the entry with that night.' },
        { title: 'Sleep again', text: 'No editing session. No bright screen. Finish in the morning.' },
      ],
    },
    capture: {
      eyebrow: 'Night capture', title: 'Your dream journal should work before you are fully awake.',
      lead: 'Voice recording is useful. The real difference is the workflow around it: screen off, night context, original audio and a clean handoff to Morning.',
      bullets: ['Wake-phrase night assistant', 'Voice entry attached to the night', 'Original recording preserved', 'Time and alarm stay as quiet utilities — not the product'],
      cta: 'Explore hands-free capture',
    },
    morning: {
      eyebrow: 'Morning', title: 'Wake up to the night already gathered.',
      lead: 'Dreams, fragments and other night notes should be waiting for you — not scattered across voice memos and notification history.',
      bullets: ['See what was captured overnight', 'Open the original voice entry', 'Add what returned after waking', 'Review dream signs and details over time'],
    },
    signs: {
      eyebrow: 'Your patterns', title: 'A personal dream sign matters more than a generic symbol list.',
      lead: 'The longer Somnori knows your dream history, the more useful recurring people, places, emotions and impossible situations can become.',
      bullets: ['Recurring dream signs', 'People, places and themes over time', 'Bridge into lucid-dream practice', 'Future intelligence grounded in your own history'],
    },
    beforeSleep: {
      eyebrow: 'Before sleep', title: 'Prepare the night instead of opening another sleep app.',
      lead: 'Stories, sounds, autosuggestion and dream-recall intention belong in the same loop as the dreams you capture later.',
      bullets: ['Bedtime stories', 'Nature and calm audio', 'Autosuggestion and recall intention', 'Lucid-dream practices'],
    },
    privacy: {
      eyebrow: 'Private by nature', title: 'Dreams are intimate data.',
      lead: 'Somnori is being built around clear ownership, original recordings and explicit control over what is kept, exported or removed. We only publish privacy claims that are true in the shipped build.',
    },
    final: {
      eyebrow: 'Android first', title: 'Your next dream may be gone by morning.',
      lead: 'Somnori is in active physical testing on Android. The public release comes after the night workflow is reliable enough to trust half asleep.',
      cta: 'See how Somnori works',
    },
    footer: { tagline: 'A nighttime dream journal built around the few minutes when a dream is still alive.', product: 'Product', learn: 'Learn', legal: 'Legal', privacy: 'Privacy', terms: 'Terms', global: 'Somnori is built for dreamers worldwide.' },
    phone: {
      nightTitle: 'Night Assistant', waiting: 'Microphone ready · waiting', heard: 'Phrase heard', recording: 'Recording dream…', original: 'Original audio saved',
      morningTitle: 'Good morning', morningSub: 'Your night in Somnori', dreamOne: 'The station above the sea', dreamTwo: 'A room with no ceiling', review: 'Review dream',
      signsTitle: 'Dream signs', recurring: 'Recurring in your dreams', signOne: 'Train stations', signTwo: 'Old houses', signThree: 'Blue water',
      sleepTitle: 'Before sleep', practice: 'Recall intention', story: 'The path you do not need to see', sound: 'Forest at night', ready: 'Night mode ready',
    },
  },
  ru: {
    metaTitle: 'Somnori — запишите сон, пока он не исчез',
    metaDescription: 'Somnori — ночной дневник сновидений для Android: бесконтактная голосовая запись, утренний разбор и личная история снов.',
    skip: 'К содержанию',
    nav: { product: 'Продукт', how: 'Как работает', morning: 'Утро', learn: 'О снах', app: 'Android', language: 'Язык' },
    hero: {
      eyebrow: 'Сон исчезает очень быстро',
      title: 'Запишите сон, не просыпаясь окончательно.',
      lead: 'Проснулись после сна — скажите фразу Somnori, расскажите его с закрытыми глазами и снова засыпайте.',
      primary: 'Как это работает ночью',
      secondary: 'О дневнике снов',
      note: 'Сначала Android. Публичный релиз готовится.',
    },
    proof: [
      { title: 'Без разблокировки', text: 'Для момента, когда совсем не хочется просыпаться.' },
      { title: 'Без печати', text: 'Расскажите сон, пока его фрагменты ещё рядом.' },
      { title: 'Исходное аудио', text: 'Сохраняется ваш голос, а не только обработанный текст.' },
      { title: 'Утро в Somnori', text: 'Вернитесь ко всей ночи уже после пробуждения.' },
    ],
    flow: {
      eyebrow: 'Создано для трёх часов ночи',
      title: 'Меньше действий между пробуждением и воспоминанием',
      lead: 'Somnori не пытается заменить системного ассистента. Он создан для одного хрупкого момента: поймать сон до того, как память начнёт распадаться.',
      steps: [
        { title: 'Проснуться', text: 'Сцена, голос или ощущение ещё удерживаются в памяти.' },
        { title: 'Позвать Somnori', text: 'Ночной помощник запускается без навигации по телефону.' },
        { title: 'Рассказать сон', text: 'Говорите естественно — запись останется внутри этой ночи.' },
        { title: 'Снова заснуть', text: 'Никакого редактирования и яркого экрана. Разберётесь утром.' },
      ],
    },
    capture: {
      eyebrow: 'Ночная запись', title: 'Дневник снов должен работать ещё до того, как вы окончательно проснулись.',
      lead: 'Голосовая запись сама по себе уже не редкость. Для Somnori важен весь ночной сценарий: экран погашен, контекст ночи сохранён, исходное аудио ждёт утром.',
      bullets: ['Ночной помощник с голосовой фразой', 'Запись привязана к конкретной ночи', 'Исходное аудио сохраняется', 'Время и будильник остаются тихими утилитами, а не главным продуктом'],
      cta: 'Бесконтактная запись подробнее',
    },
    morning: {
      eyebrow: 'Утро', title: 'Проснитесь — ночь уже собрана в одном месте.',
      lead: 'Сны, фрагменты и ночные мысли должны ждать вас в Somnori, а не быть разбросаны по диктофону и заметкам.',
      bullets: ['Посмотреть всё, что записалось ночью', 'Открыть исходную голосовую запись', 'Добавить то, что вспомнилось утром', 'Со временем отмечать детали и признаки сна'],
    },
    signs: {
      eyebrow: 'Ваши закономерности', title: 'Личный признак сна ценнее универсального сонника.',
      lead: 'Чем длиннее история снов, тем полезнее становятся повторяющиеся люди, места, эмоции и невозможные ситуации именно из ваших сновидений.',
      bullets: ['Повторяющиеся признаки сна', 'Люди, места и темы во времени', 'Мост к практике осознанных сновидений', 'Будущий анализ, основанный на вашей собственной истории'],
    },
    beforeSleep: {
      eyebrow: 'Перед сном', title: 'Подготовьте ночь, не открывая ещё одно приложение для сна.',
      lead: 'Истории, звуки, самовнушение и намерение вспомнить сон логично соединить с тем, что Somnori будет записывать ночью.',
      bullets: ['Истории перед сном', 'Звуки природы и спокойная музыка', 'Самовнушение и намерение запомнить сон', 'Практики осознанных сновидений'],
    },
    privacy: {
      eyebrow: 'Личное остаётся личным', title: 'Сновидения — очень интимные данные.',
      lead: 'Somnori строится вокруг понятного владения данными, исходных записей и явного контроля над тем, что хранится, экспортируется или удаляется. На сайте мы заявляем только то, что действительно реализовано в выпущенной версии.',
    },
    final: {
      eyebrow: 'Сначала Android', title: 'Следующий сон может исчезнуть ещё до утра.',
      lead: 'Somnori проходит физическое тестирование на Android. Публичный релиз появится после того, как ночному сценарию можно будет доверять даже в полусне.',
      cta: 'Посмотреть, как работает Somnori',
    },
    footer: { tagline: 'Ночной дневник сновидений для тех нескольких минут, пока сон ещё жив в памяти.', product: 'Продукт', learn: 'О снах', legal: 'Документы', privacy: 'Конфиденциальность', terms: 'Условия', global: 'Somnori создаётся для людей по всему миру.' },
    phone: {
      nightTitle: 'Ночной помощник', waiting: 'Микрофон готов · жду команду', heard: 'Команда услышана', recording: 'Записываю сон…', original: 'Исходное аудио сохранено',
      morningTitle: 'Доброе утро', morningSub: 'Ваша ночь в Somnori', dreamOne: 'Станция над морем', dreamTwo: 'Комната без потолка', review: 'Разобрать сон',
      signsTitle: 'Признаки сна', recurring: 'Повторяется в ваших снах', signOne: 'Вокзалы', signTwo: 'Старые дома', signThree: 'Синяя вода',
      sleepTitle: 'Перед сном', practice: 'Намерение вспомнить сон', story: 'Тропа, которой не нужно видеть всю дорогу', sound: 'Ночной лес', ready: 'Ночной режим готов',
    },
  },
  es: {
    metaTitle: 'Somnori — captura tus sueños antes de que desaparezcan',
    metaDescription: 'Somnori es un diario nocturno de sueños para Android con captura por voz, revisión matinal e historial personal.',
    skip: 'Ir al contenido',
    nav: { product: 'Producto', how: 'Cómo funciona', morning: 'Mañana', learn: 'Aprender', app: 'Android', language: 'Idioma' },
    hero: { eyebrow: 'Los sueños se desvanecen rápido', title: 'Captura el sueño. Sigue medio dormido.', lead: 'Despierta de un sueño, di tu frase de Somnori, cuéntalo con los ojos cerrados y vuelve a dormir.', primary: 'Ver el flujo nocturno', secondary: 'Explorar el diario', note: 'Primero en Android. El lanzamiento público está en preparación.' },
    proof: [
      { title: 'Sin desbloquear', text: 'Pensado para cuando no quieres despertarte del todo.' },
      { title: 'Sin escribir', text: 'Habla antes de que se pierdan los fragmentos.' },
      { title: 'Audio original', text: 'Conserva tu voz, no solo el texto procesado.' },
      { title: 'Revisión matinal', text: 'Vuelve a toda la noche cuando estés despierto.' },
    ],
    flow: { eyebrow: 'Hecho para las 3 de la mañana', title: 'Menos fricción entre despertar y recordar', lead: 'Somnori no intenta sustituir al asistente del teléfono. Está hecho para un momento frágil: atrapar el sueño antes de que el recuerdo se rompa.', steps: [
      { title: 'Despierta', text: 'Aún queda una escena, una voz o una sensación.' },
      { title: 'Di Somnori', text: 'Inicia el asistente nocturno sin navegar por el móvil.' },
      { title: 'Cuenta el sueño', text: 'Habla con naturalidad. La entrada queda unida a esa noche.' },
      { title: 'Vuelve a dormir', text: 'Sin editar ni mirar una pantalla brillante. Termina por la mañana.' },
    ] },
    capture: { eyebrow: 'Captura nocturna', title: 'Tu diario debería funcionar antes de que estés completamente despierto.', lead: 'La voz es solo una parte. La diferencia está en el flujo completo: pantalla apagada, contexto nocturno, audio original y una mañana ordenada.', bullets: ['Asistente nocturno por frase de voz', 'Entrada vinculada a la noche', 'Audio original conservado', 'Hora y alarma como utilidades discretas'], cta: 'Ver la captura manos libres' },
    morning: { eyebrow: 'Mañana', title: 'Despierta con la noche ya reunida.', lead: 'Sueños, fragmentos y notas nocturnas deberían esperarte en un solo lugar.', bullets: ['Revisa lo capturado durante la noche', 'Abre la grabación original', 'Añade lo que recuerdes al despertar', 'Sigue detalles y señales con el tiempo'] },
    signs: { eyebrow: 'Tus patrones', title: 'Una señal personal vale más que una lista genérica de símbolos.', lead: 'Con una historia más larga, las personas, lugares, emociones y situaciones que se repiten pueden volverse útiles.', bullets: ['Señales de sueño recurrentes', 'Personas, lugares y temas', 'Puente hacia los sueños lúcidos', 'Inteligencia futura basada en tu propia historia'] },
    beforeSleep: { eyebrow: 'Antes de dormir', title: 'Prepara la noche dentro del mismo ciclo.', lead: 'Historias, sonidos, autosugestión e intención de recordar pueden formar parte del mismo sistema que captura tus sueños.', bullets: ['Historias para dormir', 'Sonidos de naturaleza', 'Autosugestión e intención de recuerdo', 'Prácticas de sueño lúcido'] },
    privacy: { eyebrow: 'Privado por naturaleza', title: 'Los sueños son datos íntimos.', lead: 'Somnori se diseña alrededor de la propiedad clara de tus datos y el control explícito sobre lo que se guarda, exporta o elimina.' },
    final: { eyebrow: 'Primero Android', title: 'Tu próximo sueño puede desaparecer antes de la mañana.', lead: 'Somnori está en pruebas físicas activas en Android. El lanzamiento público llegará cuando el flujo nocturno sea suficientemente fiable.', cta: 'Ver cómo funciona Somnori' },
    footer: { tagline: 'Un diario nocturno creado para los minutos en que el sueño todavía sigue vivo.', product: 'Producto', learn: 'Aprender', legal: 'Legal', privacy: 'Privacidad', terms: 'Términos', global: 'Somnori está hecho para soñadores de todo el mundo.' },
    phone: { nightTitle: 'Asistente nocturno', waiting: 'Micrófono listo · esperando', heard: 'Frase detectada', recording: 'Grabando sueño…', original: 'Audio original guardado', morningTitle: 'Buenos días', morningSub: 'Tu noche en Somnori', dreamOne: 'La estación sobre el mar', dreamTwo: 'Una habitación sin techo', review: 'Revisar sueño', signsTitle: 'Señales del sueño', recurring: 'Se repite en tus sueños', signOne: 'Estaciones', signTwo: 'Casas antiguas', signThree: 'Agua azul', sleepTitle: 'Antes de dormir', practice: 'Intención de recordar', story: 'El camino que no necesitas ver entero', sound: 'Bosque nocturno', ready: 'Modo nocturno listo' },
  },
  de: {
    metaTitle: 'Somnori — Träume festhalten, bevor sie verblassen',
    metaDescription: 'Somnori ist ein nächtliches Traumtagebuch für Android: Sprachaufnahme, Morgenrückblick und persönliche Traumgeschichte.',
    skip: 'Zum Inhalt',
    nav: { product: 'Produkt', how: 'So funktioniert es', morning: 'Morgen', learn: 'Entdecken', app: 'Android', language: 'Sprache' },
    hero: { eyebrow: 'Träume verblassen schnell', title: 'Den Traum festhalten. Halb im Schlaf bleiben.', lead: 'Aus einem Traum aufwachen, deine Somnori-Phrase sagen, mit geschlossenen Augen erzählen und wieder einschlafen.', primary: 'Nachtablauf ansehen', secondary: 'Traumtagebuch entdecken', note: 'Android zuerst. Der öffentliche Start wird vorbereitet.' },
    proof: [
      { title: 'Ohne Entsperren', text: 'Für den Moment, in dem du nicht ganz wach werden willst.' },
      { title: 'Ohne Tippen', text: 'Sprich, bevor die Fragmente verschwinden.' },
      { title: 'Originalaudio', text: 'Bewahre deine Stimme, nicht nur bereinigten Text.' },
      { title: 'Morgenrückblick', text: 'Kehre wach zur ganzen Nacht zurück.' },
    ],
    flow: { eyebrow: 'Für 3 Uhr morgens gebaut', title: 'Weniger Reibung zwischen Aufwachen und Erinnern', lead: 'Somnori will nicht den Telefonassistenten ersetzen. Es ist für einen empfindlichen Moment gebaut: den Traum festhalten, bevor die Erinnerung zerfällt.', steps: [
      { title: 'Aufwachen', text: 'Eine Szene, Stimme oder Stimmung ist noch da.' },
      { title: 'Somnori sagen', text: 'Den Nachtassistenten starten, ohne durchs Telefon zu navigieren.' },
      { title: 'Traum erzählen', text: 'Natürlich sprechen. Der Eintrag bleibt mit dieser Nacht verbunden.' },
      { title: 'Weiterschlafen', text: 'Keine Bearbeitung, kein helles Display. Am Morgen weitermachen.' },
    ] },
    capture: { eyebrow: 'Nachtaufnahme', title: 'Ein Traumtagebuch sollte funktionieren, bevor du ganz wach bist.', lead: 'Sprachaufnahme allein ist nicht der Unterschied. Entscheidend ist der Ablauf: Display aus, Nachtkontext, Originalaudio und ein sauberer Übergang in den Morgen.', bullets: ['Nachtassistent per Sprachphrase', 'Eintrag gehört zur jeweiligen Nacht', 'Originalaudio bleibt erhalten', 'Uhrzeit und Wecker bleiben stille Hilfsfunktionen'], cta: 'Freihändige Aufnahme ansehen' },
    morning: { eyebrow: 'Morgen', title: 'Aufwachen — die Nacht ist schon gesammelt.', lead: 'Träume, Fragmente und nächtliche Notizen warten an einem Ort statt verteilt über verschiedene Apps.', bullets: ['Alle Nachtaufnahmen sehen', 'Originalaufnahme öffnen', 'Morgendliche Erinnerungen ergänzen', 'Traumzeichen und Details langfristig verfolgen'] },
    signs: { eyebrow: 'Deine Muster', title: 'Ein persönliches Traumzeichen ist wertvoller als eine allgemeine Symbol-Liste.', lead: 'Mit wachsender Traumgeschichte können wiederkehrende Menschen, Orte, Gefühle und unmögliche Situationen Bedeutung für dich gewinnen.', bullets: ['Wiederkehrende Traumzeichen', 'Menschen, Orte und Themen im Verlauf', 'Brücke zum Klarträumen', 'Zukünftige Auswertung auf Basis deiner Geschichte'] },
    beforeSleep: { eyebrow: 'Vor dem Schlafen', title: 'Bereite die Nacht im selben System vor.', lead: 'Geschichten, Klänge, Autosuggestion und Erinnerungsabsicht gehören in denselben Ablauf wie die später erfassten Träume.', bullets: ['Schlafgeschichten', 'Naturklänge', 'Autosuggestion und Traum-Erinnerungsabsicht', 'Klartraum-Übungen'] },
    privacy: { eyebrow: 'Von Natur aus privat', title: 'Träume sind intime Daten.', lead: 'Somnori wird mit klarer Datenhoheit und expliziter Kontrolle darüber entwickelt, was gespeichert, exportiert oder gelöscht wird.' },
    final: { eyebrow: 'Android zuerst', title: 'Der nächste Traum kann bis zum Morgen verschwunden sein.', lead: 'Somnori wird aktiv auf echten Android-Geräten getestet. Der öffentliche Start folgt, wenn der Nachtablauf zuverlässig genug ist.', cta: 'So funktioniert Somnori' },
    footer: { tagline: 'Ein nächtliches Traumtagebuch für die Minuten, in denen der Traum noch lebendig ist.', product: 'Produkt', learn: 'Entdecken', legal: 'Rechtliches', privacy: 'Datenschutz', terms: 'Bedingungen', global: 'Somnori ist für Träumende weltweit gedacht.' },
    phone: { nightTitle: 'Nachtassistent', waiting: 'Mikrofon bereit · warte', heard: 'Phrase erkannt', recording: 'Traum wird aufgenommen…', original: 'Originalaudio gespeichert', morningTitle: 'Guten Morgen', morningSub: 'Deine Nacht in Somnori', dreamOne: 'Der Bahnhof über dem Meer', dreamTwo: 'Ein Zimmer ohne Decke', review: 'Traum ansehen', signsTitle: 'Traumzeichen', recurring: 'Wiederholt sich in deinen Träumen', signOne: 'Bahnhöfe', signTwo: 'Alte Häuser', signThree: 'Blaues Wasser', sleepTitle: 'Vor dem Schlafen', practice: 'Erinnerungsabsicht', story: 'Der Weg, den du nicht ganz sehen musst', sound: 'Nachtwald', ready: 'Nachtmodus bereit' },
  },
  fr: {
    metaTitle: 'Somnori — capturez vos rêves avant qu’ils ne s’effacent',
    metaDescription: 'Somnori est un journal de rêves nocturne pour Android : capture vocale, revue du matin et histoire personnelle de vos rêves.',
    skip: 'Aller au contenu',
    nav: { product: 'Produit', how: 'Comment ça marche', morning: 'Matin', learn: 'Découvrir', app: 'Android', language: 'Langue' },
    hero: { eyebrow: 'Les rêves s’effacent vite', title: 'Capturez le rêve. Restez à moitié endormi.', lead: 'Réveillez-vous d’un rêve, dites votre phrase Somnori, racontez-le les yeux fermés puis rendormez-vous.', primary: 'Voir le parcours nocturne', secondary: 'Découvrir le journal', note: 'Android d’abord. Le lancement public est en préparation.' },
    proof: [
      { title: 'Sans déverrouiller', text: 'Pour le moment où vous ne voulez pas vous réveiller complètement.' },
      { title: 'Sans taper', text: 'Parlez avant que les fragments ne disparaissent.' },
      { title: 'Audio original', text: 'Gardez votre voix, pas seulement un texte nettoyé.' },
      { title: 'Revue du matin', text: 'Retrouvez toute la nuit une fois bien réveillé.' },
    ],
    flow: { eyebrow: 'Pensé pour 3 h du matin', title: 'Moins de friction entre le réveil et le souvenir', lead: 'Somnori ne cherche pas à remplacer l’assistant du téléphone. Il est conçu pour un moment fragile : saisir le rêve avant que le souvenir ne se défasse.', steps: [
      { title: 'Se réveiller', text: 'Une scène, une voix ou une sensation est encore présente.' },
      { title: 'Dire Somnori', text: 'Lancer l’assistant nocturne sans naviguer dans le téléphone.' },
      { title: 'Raconter le rêve', text: 'Parlez naturellement. L’entrée reste liée à cette nuit.' },
      { title: 'Se rendormir', text: 'Pas d’édition, pas d’écran lumineux. Vous finirez le matin.' },
    ] },
    capture: { eyebrow: 'Capture nocturne', title: 'Votre journal devrait fonctionner avant votre réveil complet.', lead: 'La voix seule n’est pas la différence. Ce qui compte, c’est le parcours : écran éteint, contexte nocturne, audio original et passage propre vers le matin.', bullets: ['Assistant nocturne par phrase vocale', 'Entrée rattachée à la nuit', 'Audio original conservé', 'Heure et réveil restent des utilitaires discrets'], cta: 'Voir la capture mains libres' },
    morning: { eyebrow: 'Matin', title: 'Réveillez-vous : la nuit est déjà rassemblée.', lead: 'Rêves, fragments et notes nocturnes devraient vous attendre au même endroit.', bullets: ['Voir ce qui a été capturé pendant la nuit', 'Ouvrir l’enregistrement original', 'Ajouter ce qui revient au réveil', 'Suivre détails et signes au fil du temps'] },
    signs: { eyebrow: 'Vos motifs', title: 'Un signe de rêve personnel vaut mieux qu’une liste générique de symboles.', lead: 'Avec le temps, les personnes, lieux, émotions et situations impossibles qui se répètent peuvent devenir utiles.', bullets: ['Signes de rêve récurrents', 'Personnes, lieux et thèmes dans le temps', 'Passerelle vers le rêve lucide', 'Future intelligence fondée sur votre propre histoire'] },
    beforeSleep: { eyebrow: 'Avant de dormir', title: 'Préparez la nuit dans le même cycle.', lead: 'Histoires, sons, autosuggestion et intention de se souvenir peuvent faire partie du même système que la capture nocturne.', bullets: ['Histoires du soir', 'Sons de la nature', 'Autosuggestion et intention de rappel', 'Pratiques de rêve lucide'] },
    privacy: { eyebrow: 'Privé par nature', title: 'Les rêves sont des données intimes.', lead: 'Somnori est conçu autour d’une propriété claire des données et d’un contrôle explicite sur ce qui est conservé, exporté ou supprimé.' },
    final: { eyebrow: 'Android d’abord', title: 'Votre prochain rêve peut disparaître avant le matin.', lead: 'Somnori est activement testé sur de vrais appareils Android. Le lancement public viendra lorsque le parcours nocturne sera suffisamment fiable.', cta: 'Voir comment fonctionne Somnori' },
    footer: { tagline: 'Un journal de rêves nocturne pour les quelques minutes où le rêve est encore vivant.', product: 'Produit', learn: 'Découvrir', legal: 'Mentions', privacy: 'Confidentialité', terms: 'Conditions', global: 'Somnori est conçu pour les rêveurs du monde entier.' },
    phone: { nightTitle: 'Assistant nocturne', waiting: 'Micro prêt · en attente', heard: 'Phrase reconnue', recording: 'Enregistrement du rêve…', original: 'Audio original sauvegardé', morningTitle: 'Bonjour', morningSub: 'Votre nuit dans Somnori', dreamOne: 'La gare au-dessus de la mer', dreamTwo: 'Une pièce sans plafond', review: 'Revoir le rêve', signsTitle: 'Signes de rêve', recurring: 'Revient dans vos rêves', signOne: 'Gares', signTwo: 'Vieilles maisons', signThree: 'Eau bleue', sleepTitle: 'Avant de dormir', practice: 'Intention de se souvenir', story: 'Le chemin qu’il n’est pas nécessaire de voir en entier', sound: 'Forêt nocturne', ready: 'Mode nuit prêt' },
  },
  tr: {
    metaTitle: 'Somnori — rüyalar kaybolmadan önce yakala',
    metaDescription: 'Somnori, Android için gece rüya günlüğü: sesle kayıt, sabah incelemesi ve kişisel rüya geçmişi.',
    skip: 'İçeriğe geç',
    nav: { product: 'Ürün', how: 'Nasıl çalışır', morning: 'Sabah', learn: 'Keşfet', app: 'Android', language: 'Dil' },
    hero: { eyebrow: 'Rüyalar hızla silinir', title: 'Rüyayı yakala. Yarı uykuda kal.', lead: 'Bir rüyadan uyan, Somnori cümleni söyle, gözlerin kapalıyken anlat ve tekrar uyu.', primary: 'Gece akışını gör', secondary: 'Rüya günlüğünü keşfet', note: 'Önce Android. Genel yayın hazırlanıyor.' },
    proof: [
      { title: 'Kilidi açmadan', text: 'Tamamen uyanmak istemediğin an için tasarlandı.' },
      { title: 'Yazmadan', text: 'Parçalar kaybolmadan önce konuş.' },
      { title: 'Orijinal ses', text: 'Yalnızca işlenmiş metni değil, kendi sesini de sakla.' },
      { title: 'Sabah incelemesi', text: 'Tamamen uyandığında bütün geceye geri dön.' },
    ],
    flow: { eyebrow: 'Gece 3 için tasarlandı', title: 'Uyanmakla hatırlamak arasındaki sürtünmeyi azalt', lead: 'Somnori telefon asistanının yerini almaya çalışmaz. Tek bir hassas an için tasarlanmıştır: rüya hafızası dağılmadan onu yakalamak.', steps: [
      { title: 'Uyan', text: 'Bir sahne, ses ya da his hâlâ aklında.' },
      { title: 'Somnori de', text: 'Telefonda gezinmeden gece asistanını başlat.' },
      { title: 'Rüyayı anlat', text: 'Doğal konuş. Kayıt o geceyle birlikte kalır.' },
      { title: 'Tekrar uyu', text: 'Düzenleme yok, parlak ekran yok. Sabah tamamlarsın.' },
    ] },
    capture: { eyebrow: 'Gece kaydı', title: 'Rüya günlüğün tamamen uyanmadan önce çalışmalı.', lead: 'Ses kaydı tek başına fark değildir. Fark; ekran kapalıyken gece bağlamı, orijinal ses ve sabaha düzgün geçiştir.', bullets: ['Sesli ifadeyle gece asistanı', 'Kayıt o geceye bağlı kalır', 'Orijinal ses korunur', 'Saat ve alarm sessiz yardımcılar olarak kalır'], cta: 'Temassız kaydı gör' },
    morning: { eyebrow: 'Sabah', title: 'Uyandığında gece zaten bir araya gelmiş olsun.', lead: 'Rüyalar, parçalar ve gece notları farklı uygulamalara dağılmak yerine tek yerde seni beklemeli.', bullets: ['Gece yakalananları gör', 'Orijinal ses kaydını aç', 'Sabah geri gelenleri ekle', 'Zamanla ayrıntıları ve rüya işaretlerini izle'] },
    signs: { eyebrow: 'Senin örüntülerin', title: 'Kişisel bir rüya işareti, genel bir sembol listesinden daha değerlidir.', lead: 'Rüya geçmişin büyüdükçe tekrar eden kişiler, yerler, duygular ve imkânsız durumlar daha anlamlı hale gelebilir.', bullets: ['Tekrarlayan rüya işaretleri', 'Zaman içinde kişiler, yerler ve temalar', 'Berrak rüya pratiğine köprü', 'Kendi geçmişine dayalı gelecekteki analiz'] },
    beforeSleep: { eyebrow: 'Uyumadan önce', title: 'Geceyi aynı döngü içinde hazırla.', lead: 'Hikâyeler, sesler, oto-sugestiyon ve rüyayı hatırlama niyeti daha sonra kaydedeceğin rüyalarla aynı sistemde yer alabilir.', bullets: ['Uyku hikâyeleri', 'Doğa sesleri', 'Oto-sugestiyon ve hatırlama niyeti', 'Berrak rüya pratikleri'] },
    privacy: { eyebrow: 'Doğası gereği özel', title: 'Rüyalar mahrem verilerdir.', lead: 'Somnori, verilerinin kime ait olduğunun açık olduğu ve neyin saklanacağı, dışa aktarılacağı ya da silineceği üzerinde net kontrol sağlanan bir yapı ile geliştiriliyor.' },
    final: { eyebrow: 'Önce Android', title: 'Bir sonraki rüyan sabaha kadar kaybolabilir.', lead: 'Somnori gerçek Android cihazlarda aktif olarak test ediliyor. Genel yayın, gece akışı yeterince güvenilir olduğunda gelecek.', cta: 'Somnori nasıl çalışır?' },
    footer: { tagline: 'Rüyanın hâlâ canlı olduğu birkaç dakika için tasarlanmış gece rüya günlüğü.', product: 'Ürün', learn: 'Keşfet', legal: 'Yasal', privacy: 'Gizlilik', terms: 'Koşullar', global: 'Somnori dünyanın dört bir yanındaki rüya görenler için geliştiriliyor.' },
    phone: { nightTitle: 'Gece asistanı', waiting: 'Mikrofon hazır · bekliyor', heard: 'İfade algılandı', recording: 'Rüya kaydediliyor…', original: 'Orijinal ses kaydedildi', morningTitle: 'Günaydın', morningSub: 'Somnori’de gecen', dreamOne: 'Denizin üzerindeki istasyon', dreamTwo: 'Tavansız bir oda', review: 'Rüyayı incele', signsTitle: 'Rüya işaretleri', recurring: 'Rüyalarında tekrarlanıyor', signOne: 'Tren istasyonları', signTwo: 'Eski evler', signThree: 'Mavi su', sleepTitle: 'Uyumadan önce', practice: 'Hatırlama niyeti', story: 'Tamamını görmen gerekmeyen yol', sound: 'Gece ormanı', ready: 'Gece modu hazır' },
  },
};
