import type { PublicLocale } from './public';

export type HomeV21Copy = {
  metaTitle: string;
  metaDescription: string;
  hero: { eyebrow: string; title: string; lead: string; primary: string; secondary: string; note: string; availability: string };
  proof: { title: string; text: string }[];
  flow: { eyebrow: string; title: string; lead: string; steps: { title: string; text: string }[] };
  capture: { eyebrow: string; title: string; lead: string; bullets: string[]; cta: string };
  morning: { eyebrow: string; title: string; lead: string; bullets: string[] };
  signs: { eyebrow: string; title: string; lead: string; bullets: string[] };
  beforeSleep: { eyebrow: string; title: string; lead: string; bullets: string[] };
  privacy: { eyebrow: string; title: string; lead: string };
  final: { eyebrow: string; title: string; lead: string; cta: string };
};

export const homeV21: Record<PublicLocale, HomeV21Copy> = {
  en: {
    metaTitle: 'Somnori — Tell Your Dream Before It Fades',
    metaDescription: 'Somnori is an Android-first dream journal built for the moment you wake from a dream: hands-free voice capture, original audio and a morning view of the night.',
    hero: {
      eyebrow: 'A dream can disappear before you are fully awake',
      title: 'Tell Somnori before the dream fades.',
      lead: 'Wake from a dream. Say your Somnori phrase. Describe what you remember with your eyes closed, then go back to sleep.',
      primary: 'See the night flow',
      secondary: 'Explore the dream journal',
      note: 'No unlocking. No typing. Keep the original voice.',
      availability: 'The Android app is currently in Russian. The English interface is in preparation.',
    },
    proof: [
      { title: 'No unlock', text: 'Start the night flow without navigating through the phone.' },
      { title: 'No typing', text: 'Say the fragment while it is still vivid.' },
      { title: 'Original voice', text: 'The recording stays with the dream entry.' },
      { title: 'Morning view', text: 'Come back to the whole night when you are fully awake.' },
    ],
    flow: {
      eyebrow: 'Made for the middle of the night',
      title: 'Wake. Speak. Sleep again.',
      lead: 'Somnori is designed to keep the gap between remembering a dream and saving it as small and quiet as possible.',
      steps: [
        { title: 'Wake', text: 'A scene, place, person or feeling is still there.' },
        { title: 'Call Somnori', text: 'Use your night phrase instead of opening and navigating an app.' },
        { title: 'Tell the dream', text: 'Speak naturally. Save the fragment before it breaks apart.' },
        { title: 'Go back to sleep', text: 'Leave sorting, reading and adding details for the morning.' },
      ],
    },
    capture: {
      eyebrow: 'Night Assistant',
      title: 'Built for the first minute after a dream.',
      lead: 'A normal voice recorder can save audio. Somnori is built around the whole nighttime moment: a screen-off start, a dream entry tied to the night, and a clear handoff to Morning.',
      bullets: ['Wake-phrase night assistant', 'Dreams and thoughts saved into the current night', 'Original audio kept with the entry', 'Time and alarm remain quiet night utilities'],
      cta: 'See hands-free dream capture',
    },
    morning: {
      eyebrow: 'Morning in Somnori',
      title: 'By morning, the night is already together.',
      lead: 'Open one place and see what you captured overnight. Add the part of a dream that returned after waking, then review it when you are actually alert.',
      bullets: ['See dreams and other night entries', 'Open the original voice recording', 'Add another dream by voice', 'Review details and recurring dream signs'],
    },
    signs: {
      eyebrow: 'Somnori notices',
      title: 'Your recurring signs are more useful than a generic symbol list.',
      lead: 'When the same place, person or impossible situation returns, it becomes part of your own dream language. Somnori keeps those repetitions connected to the dreams they came from.',
      bullets: ['Recurring dream signs from your history', 'People, places and unusual situations', 'A bridge to lucid-dream practice', 'A foundation for deeper personal dream intelligence'],
    },
    beforeSleep: {
      eyebrow: 'Before sleep',
      title: 'The next dream starts before you fall asleep.',
      lead: 'Somnori brings the preparation into the same night loop: calming audio, practices, autosuggestion and a simple intention to remember what comes next.',
      bullets: ['Calm music and nature audio', 'Before-sleep practices', 'Autosuggestion and dream-recall intention', 'Lucid-dream preparation'],
    },
    privacy: {
      eyebrow: 'Private by nature',
      title: 'A dream journal holds unusually personal material.',
      lead: 'Somnori is being built around clear ownership of entries and recordings. The public site only promises privacy and export behavior that is actually verified in the shipped app.',
    },
    final: {
      eyebrow: 'Android first',
      title: 'The useful moment is the one before the dream is gone.',
      lead: 'We are testing the Russian Android build on real devices now. English is the next interface localization; the website is already being prepared for the international launch.',
      cta: 'See how the night flow works',
    },
  },
  ru: {
    metaTitle: 'Somnori — расскажите сон, пока он не исчез',
    metaDescription: 'Somnori — дневник сновидений для Android, созданный для первых минут после сна: бесконтактная голосовая запись, исходное аудио и утренний обзор ночи.',
    hero: {
      eyebrow: 'Сон может исчезнуть раньше, чем вы окончательно проснётесь',
      title: 'Расскажите Somnori, пока сон не исчез.',
      lead: 'Проснулись после сна — позовите Somnori, расскажите всё, что помните, не открывая глаз, и снова засыпайте.',
      primary: 'Посмотреть ночной сценарий',
      secondary: 'Что происходит утром',
      note: 'Без разблокировки. Без печати. С сохранением исходного голоса.',
      availability: 'Русская версия Android-приложения сейчас проходит тестирование на реальных устройствах.',
    },
    proof: [
      { title: 'Без разблокировки', text: 'Не нужно искать приложение и попадать в нужный экран.' },
      { title: 'Без печати', text: 'Расскажите фрагмент, пока он ещё жив в памяти.' },
      { title: 'Исходный голос', text: 'Запись остаётся рядом с самим сном.' },
      { title: 'Утро в Somnori', text: 'Вернитесь ко всей ночи уже после пробуждения.' },
    ],
    flow: {
      eyebrow: 'Создано для середины ночи',
      title: 'Проснулись. Рассказали. Снова спите.',
      lead: 'Задача Somnori — сделать промежуток между воспоминанием о сне и его сохранением как можно короче и спокойнее.',
      steps: [
        { title: 'Проснулись', text: 'В памяти ещё держится сцена, место, человек или ощущение.' },
        { title: 'Позвали Somnori', text: 'Используйте ночную фразу вместо разблокировки и навигации по телефону.' },
        { title: 'Рассказали сон', text: 'Говорите естественно. Главное — успеть сохранить то, что ещё помните.' },
        { title: 'Снова заснули', text: 'Читать, дополнять и разбирать сон можно уже утром.' },
      ],
    },
    capture: {
      eyebrow: 'Ночной помощник',
      title: 'Для первой минуты после сна.',
      lead: 'Обычный диктофон тоже умеет сохранять голос. Somnori создаётся вокруг всего ночного сценария: запуск без навигации, запись внутри конкретной ночи и понятное продолжение утром.',
      bullets: ['Ночной помощник с голосовой фразой', 'Сны и мысли сохраняются внутри текущей ночи', 'Исходное аудио остаётся вместе с записью', 'Время и будильник работают как спокойные ночные утилиты'],
      cta: 'Подробнее о бесконтактной записи',
    },
    morning: {
      eyebrow: 'Утро в Somnori',
      title: 'К утру ночь уже собрана.',
      lead: 'Откройте один экран и посмотрите всё, что записали ночью. Добавьте голосом то, что вспомнилось после пробуждения, и спокойно разберите сон.',
      bullets: ['Сны и другие ночные записи в одном месте', 'Исходная голосовая запись рядом', 'Можно добавить ещё один сон голосом', 'Детали и повторяющиеся признаки остаются в истории'],
    },
    signs: {
      eyebrow: 'Somnori замечает',
      title: 'Ваши повторяющиеся признаки важнее универсального сонника.',
      lead: 'Если одно и то же место, человек или невозможная ситуация возвращаются снова, это становится частью именно вашей истории сновидений. Somnori связывает такие повторы с конкретными снами.',
      bullets: ['Повторяющиеся признаки из вашей истории', 'Люди, места и необычные ситуации', 'Мост к практике осознанных сновидений', 'Основа для более глубокого персонального анализа'],
    },
    beforeSleep: {
      eyebrow: 'Перед сном',
      title: 'Следующий сон начинается ещё до засыпания.',
      lead: 'Подготовка остаётся в том же ночном цикле: спокойный звук, практика, самовнушение и простое намерение запомнить то, что приснится.',
      bullets: ['Спокойная музыка и звуки природы', 'Практики перед сном', 'Самовнушение и намерение запомнить сон', 'Подготовка к осознанным сновидениям'],
    },
    privacy: {
      eyebrow: 'Личное по своей природе',
      title: 'Дневник снов хранит очень личный материал.',
      lead: 'Somnori строится вокруг понятного владения записями и исходным аудио. На публичном сайте мы обещаем только те возможности конфиденциальности и экспорта, которые реально проверены в выпущенной версии.',
    },
    final: {
      eyebrow: 'Сначала Android',
      title: 'Главный момент — пока сон ещё не исчез.',
      lead: 'Русская Android-версия проходит тестирование на реальных устройствах. После принятия ночного сценария мы перейдём к публичному релизу и следующим языкам интерфейса.',
      cta: 'Посмотреть, как работает ночь',
    },
  },
};
