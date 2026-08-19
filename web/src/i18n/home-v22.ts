import type { PublicLocale } from './public';

export type HomeV22Copy = {
  metaTitle: string;
  metaDescription: string;
  nav: { product: string; capture: string; routine: string; dreams: string; app: string; language: string };
  hero: { eyebrow: string; title: string; lead: string; primary: string; secondary: string; note: string; availability: string };
  pillars: { title: string; text: string; icon: string }[];
  capture: { eyebrow: string; title: string; lead: string; bullets: string[]; quote: string };
  handsFree: { eyebrow: string; title: string; lead: string; cards: { title: string; text: string }[] };
  bedtime: { eyebrow: string; title: string; lead: string; steps: { title: string; text: string }[]; note: string };
  wake: { eyebrow: string; badge: string; title: string; lead: string; chain: string[]; note: string };
  dreams: { eyebrow: string; title: string; lead: string; bullets: string[]; cta: string };
  features: { eyebrow: string; title: string; lead: string; items: { title: string; text: string; status: 'current' | 'next' }[]; current: string; next: string };
  privacy: { eyebrow: string; title: string; lead: string };
  final: { eyebrow: string; title: string; lead: string; cta: string };
  placeholder: { home: string; capture: string; routine: string; dreams: string; caption: string };
  footer: { tagline: string; product: string; explore: string; legal: string; privacy: string; terms: string; global: string };
};

export const homeV22: Record<PublicLocale, HomeV22Copy> = {
  en: {
    metaTitle: 'Somnori — A Hands-Free Night Companion for Thoughts, Routines & Dreams',
    metaDescription: 'Somnori is an Android-first night companion for hands-free thought capture, time and alarms, bedtime routines, autosuggestion, morning review and dream journaling.',
    nav: { product: 'Product', capture: 'Night capture', routine: 'Night routines', dreams: 'Dreams', app: 'Android app', language: 'Language' },
    hero: {
      eyebrow: 'Your night, without reaching for the phone',
      title: 'Keep what comes to you at night.',
      lead: 'Ideas. Thoughts. Dreams. Ask the time, set an alarm, save what matters, or start the routine you chose — without turning the night into screen time.',
      primary: 'Explore the night system',
      secondary: 'See dream features',
      note: 'Hands-free capture is the core. Dreams are one powerful part of a larger night system.',
      availability: 'The current Android build is in Russian. English app localization comes after the Russian product flow is approved.',
    },
    pillars: [
      { icon: '✦', title: 'Capture', text: 'Save a thought, idea or dream before sleep erases it.' },
      { icon: '◷', title: 'Night', text: 'Ask the time and manage the alarm without navigating the phone.' },
      { icon: '◐', title: 'Routine', text: 'Bring sound, practices and autosuggestion into one bedtime flow.' },
      { icon: '☾', title: 'Dreams', text: 'Record, review and build a personal dream history over time.' },
    ],
    capture: {
      eyebrow: 'Thoughts before they disappear',
      title: 'The idea at 2:47 AM can be more valuable than the dream.',
      lead: 'Somnori is built for the moment when opening Notes, typing a sentence and looking at a bright screen is enough to lose both the thought and the chance to fall asleep again.',
      bullets: ['Record a thought or idea by voice', 'Capture a dream with the same low-friction night flow', 'Keep the original audio with the night', 'Review what you said after waking'],
      quote: 'Never lose a thought because it came at 3 AM.',
    },
    handsFree: {
      eyebrow: 'Hands-free night utilities',
      title: 'Useful commands should not require becoming fully awake.',
      lead: 'Time and alarms are not Somnori’s marketing headline, but in the middle of the night they can be some of its most valuable everyday functions.',
      cards: [
        { title: 'What time is it?', text: 'Ask without finding the phone or lighting the screen.' },
        { title: 'Voice alarm', text: 'Set or change the alarm through the night assistant.' },
        { title: 'Night Assistant', text: 'A dedicated voice-first mode keeps night actions in one context.' },
      ],
    },
    bedtime: {
      eyebrow: 'Before sleep',
      title: 'Build the night you want to enter.',
      lead: 'Somnori already brings together pieces that usually live in separate apps: calming audio, nature sounds, practices and autosuggestion. The product direction is to make them feel like one personal bedtime protocol.',
      steps: [
        { title: 'Sound', text: 'Choose music or a quiet nature background.' },
        { title: 'Practice', text: 'Add a short preparation or lucid-dream practice.' },
        { title: 'Autosuggestion', text: 'Use an intention or self-suggestion before sleep.' },
        { title: 'Night mode', text: 'Finish with the hands-free night assistant ready.' },
      ],
      note: 'Current build: sound, practices, autosuggestion and before-sleep program elements are present. Deeper protocol composition can evolve without changing the core concept.',
    },
    wake: {
      eyebrow: 'Wake protocol',
      badge: 'NEXT PRODUCT LAYER',
      title: 'Waking up can be a sequence, not just a ringtone.',
      lead: 'The next layer is a configurable wake flow: the alarm fires, then Somnori can continue with the audio, autosuggestion or short practice the user chose beforehand.',
      chain: ['Alarm', 'Chosen audio', 'Autosuggestion', 'Morning practice'],
      note: 'Shown as product direction, not as a currently shipped 0.30 capability.',
    },
    dreams: {
      eyebrow: 'Dream layer',
      title: 'And when the night gives you a dream, Somnori can keep that too.',
      lead: 'Dreams remain a major acquisition and product layer: low-friction capture, Morning review, recurring dream signs and a path toward lucid-dream tools and personal Dream Intelligence.',
      bullets: ['Hands-free dream capture', 'Morning review with original voice', 'Recurring dream signs and history', 'Lucid-dream layer', 'Future analysis grounded in your own dream archive'],
      cta: 'Explore the dream journal',
    },
    features: {
      eyebrow: 'One night system',
      title: 'More than a dream journal. More focused than a general assistant.',
      lead: 'Somnori concentrates on the hours from settling down to fully waking up. Some pieces are already in the Russian Android build; others are deliberately shown as the next layer.',
      current: 'Current build',
      next: 'Next layer',
      items: [
        { title: 'Voice thought capture', text: 'Ideas and thoughts without typing.', status: 'current' },
        { title: 'Dream capture', text: 'Night voice entry plus Morning review.', status: 'current' },
        { title: 'Ask the time', text: 'Hands-free time request during the night.', status: 'current' },
        { title: 'Voice alarm', text: 'Set or change the alarm through voice commands.', status: 'current' },
        { title: 'Autosuggestion', text: 'Before-sleep self-suggestion and intention.', status: 'current' },
        { title: 'Soundscapes', text: 'Built-in music and nature audio.', status: 'current' },
        { title: 'Before-sleep practices', text: 'Preparation and lucid-dream routines.', status: 'current' },
        { title: 'Morning', text: 'The night gathered into one morning view.', status: 'current' },
        { title: 'Personal wake protocol', text: 'Alarm followed by selected audio or practice.', status: 'next' },
        { title: 'Dream Intelligence', text: 'Long-term patterns grounded in personal history.', status: 'next' },
      ],
    },
    privacy: {
      eyebrow: 'Private by nature',
      title: 'Night thoughts can be even more personal than dreams.',
      lead: 'Somnori’s public site will only claim storage, export and privacy behavior that is verified in the shipped app. Product positioning should never depend on promises the build cannot yet prove.',
    },
    final: {
      eyebrow: 'Android first',
      title: 'A companion for the part of the day most apps ignore.',
      lead: 'We are completing the Russian Android experience first. Once the product flow is stable, English localization and real English product screenshots become the next release step.',
      cta: 'See the full night system',
    },
    placeholder: { home: 'Night system', capture: 'Hands-free capture', routine: 'Bedtime routine', dreams: 'Dream layer', caption: 'Real product screenshot slot' },
    footer: { tagline: 'A hands-free night companion for thoughts, routines, alarms and dreams.', product: 'Product', explore: 'Explore', legal: 'Legal', privacy: 'Privacy', terms: 'Terms', global: 'Somnori is being built as one system for the whole night.' },
  },
  ru: {
    metaTitle: 'Somnori — бесконтактный ночной помощник для мыслей, сна и сновидений',
    metaDescription: 'Somnori — ночной помощник для Android: бесконтактная запись мыслей и снов, голосовые часы и будильник, музыка, самовнушение, ночные практики и утренний обзор.',
    nav: { product: 'Продукт', capture: 'Ночная запись', routine: 'Сценарий ночи', dreams: 'Сновидения', app: 'Android', language: 'Язык' },
    hero: {
      eyebrow: 'Ваша ночь — без необходимости брать телефон',
      title: 'Не теряйте то, что приходит к вам ночью.',
      lead: 'Идеи. Мысли. Сны. Спросите время, поставьте будильник, сохраните важное или запустите выбранный вечерний сценарий — не превращая ночь во время перед экраном.',
      primary: 'Посмотреть всю систему ночи',
      secondary: 'Возможности для сновидений',
      note: 'Бесконтактный ночной сценарий — ядро Somnori. Сновидения — один из сильных модулей внутри него.',
      availability: 'Русская Android-версия проходит тестирование на реальных устройствах. Реальные скриншоты добавим после фиксации полуфинального интерфейса.',
    },
    pillars: [
      { icon: '✦', title: 'Записать', text: 'Сохранить мысль, идею или сон, пока они не исчезли.' },
      { icon: '◷', title: 'Ночь', text: 'Узнать время и управлять будильником, не беря телефон.' },
      { icon: '◐', title: 'Сценарий', text: 'Соединить звук, практики и самовнушение перед сном.' },
      { icon: '☾', title: 'Сновидения', text: 'Записывать, разбирать и собирать личную историю снов.' },
    ],
    capture: {
      eyebrow: 'Мысли, пока они не исчезли',
      title: 'Идея в 2:47 ночи может быть ценнее приснившегося сна.',
      lead: 'Somnori нужен именно в тот момент, когда открыть заметки, напечатать предложение и посмотреть на яркий экран — значит потерять и мысль, и возможность быстро снова заснуть.',
      bullets: ['Записать мысль или идею голосом', 'Тем же ночным сценарием сохранить сон', 'Оставить исходное аудио внутри этой ночи', 'Утром вернуться ко всему, что было сказано'],
      quote: 'Не потерять идею только потому, что она пришла в три часа ночи.',
    },
    handsFree: {
      eyebrow: 'Бесконтактные ночные функции',
      title: 'Полезное ночью не должно требовать полного пробуждения.',
      lead: 'Время и будильник — не рекламный центр Somnori, но в реальной ночи именно эти функции могут использоваться чаще всего.',
      cards: [
        { title: 'Сколько времени?', text: 'Спросить голосом, не искать телефон и не включать экран.' },
        { title: 'Голосовой будильник', text: 'Поставить или изменить будильник через ночного помощника.' },
        { title: 'Ночной помощник', text: 'Отдельный голосовой режим удерживает все ночные действия в одном контексте.' },
      ],
    },
    bedtime: {
      eyebrow: 'Перед сном',
      title: 'Соберите ночь, в которую хотите войти.',
      lead: 'Somnori уже соединяет то, что обычно разбросано по разным приложениям: спокойную музыку, звуки природы, практики и самовнушение. Направление продукта — превратить это в единый личный протокол засыпания.',
      steps: [
        { title: 'Звук', text: 'Выберите музыку или спокойный природный фон.' },
        { title: 'Практика', text: 'Добавьте короткую подготовку или практику осознанных сновидений.' },
        { title: 'Самовнушение', text: 'Задайте намерение или текст самовнушения перед сном.' },
        { title: 'Ночной режим', text: 'Завершите сценарием с готовым бесконтактным помощником.' },
      ],
      note: 'В текущей сборке уже есть звук, практики, самовнушение и элементы программы перед сном. Более гибкая сборка протоколов может развиваться поверх этой основы.',
    },
    wake: {
      eyebrow: 'Протокол пробуждения',
      badge: 'СЛЕДУЮЩИЙ СЛОЙ ПРОДУКТА',
      title: 'Пробуждение может быть сценарием, а не просто звонком.',
      lead: 'Следующий слой Somnori — настраиваемая цепочка после срабатывания будильника: затем запускается заранее выбранный звук, самовнушение или короткая практика.',
      chain: ['Будильник', 'Выбранный звук', 'Самовнушение', 'Утренняя практика'],
      note: 'Это направление продукта, а не заявленная функция текущей версии 0.30.',
    },
    dreams: {
      eyebrow: 'Слой сновидений',
      title: 'А если ночью пришёл сон — Somnori сохранит и его.',
      lead: 'Сновидения остаются крупным маркетинговым и продуктовым направлением: бесконтактная запись, утренний разбор, повторяющиеся признаки сна и дальнейший путь к осознанным сновидениям и персональной Dream Intelligence.',
      bullets: ['Бесконтактная запись сна', 'Утренний обзор с исходным голосом', 'Повторяющиеся признаки и история снов', 'Инструменты для осознанных сновидений', 'Будущий анализ на основе именно вашей истории'],
      cta: 'О дневнике сновидений',
    },
    features: {
      eyebrow: 'Одна система ночи',
      title: 'Больше, чем дневник снов. Уже, чем универсальный ассистент.',
      lead: 'Somnori сосредоточен на часах от подготовки ко сну до окончательного пробуждения. Часть функций уже есть в русской Android-сборке, а следующий слой мы показываем отдельно и честно.',
      current: 'Есть сейчас',
      next: 'Следующий слой',
      items: [
        { title: 'Голосовая запись мыслей', text: 'Идеи и озарения без печати.', status: 'current' },
        { title: 'Запись сновидений', text: 'Ночная запись и утренний обзор.', status: 'current' },
        { title: 'Спросить время', text: 'Бесконтактный запрос времени ночью.', status: 'current' },
        { title: 'Голосовой будильник', text: 'Поставить или изменить будильник голосом.', status: 'current' },
        { title: 'Самовнушение', text: 'Намерение и самовнушение перед сном.', status: 'current' },
        { title: 'Музыка и звуки', text: 'Встроенная музыка и звуки природы.', status: 'current' },
        { title: 'Практики перед сном', text: 'Подготовка и lucid-практики.', status: 'current' },
        { title: 'Утро', text: 'Вся ночь собрана в одном утреннем экране.', status: 'current' },
        { title: 'Личный протокол пробуждения', text: 'Будильник → выбранный звук или практика.', status: 'next' },
        { title: 'Dream Intelligence', text: 'Долгосрочные закономерности из личной истории.', status: 'next' },
      ],
    },
    privacy: {
      eyebrow: 'Личное по своей природе',
      title: 'Ночные мысли могут быть даже личнее сновидений.',
      lead: 'На публичном сайте Somnori будет обещать только те правила хранения, экспорта и конфиденциальности, которые действительно подтверждены выпущенной сборкой. Позиционирование не должно зависеть от неподтверждённых обещаний.',
    },
    final: {
      eyebrow: 'Сначала Android',
      title: 'Помощник для той части суток, которую большинство приложений почти не замечает.',
      lead: 'Сначала мы доводим русскую Android-версию и фиксируем продуктовый сценарий. После этого делаем английскую локализацию приложения и уже из неё — настоящие английские скриншоты для сайта.',
      cta: 'Посмотреть всю систему ночи',
    },
    placeholder: { home: 'Система ночи', capture: 'Бесконтактная запись', routine: 'Сценарий засыпания', dreams: 'Сновидения', caption: 'Место для реального скриншота приложения' },
    footer: { tagline: 'Бесконтактный ночной помощник для мыслей, ритуалов, будильника и сновидений.', product: 'Продукт', explore: 'Разделы', legal: 'Документы', privacy: 'Конфиденциальность', terms: 'Условия', global: 'Somnori создаётся как единая система для всей ночи.' },
  },
};
