import { localeMeta, type Locale } from './site';

// Public at the current product stage. Other translations stay prepared in site.ts
// but are not routed, linked, indexed or included in the sitemap until the app UI supports them.
export const publicLocales = ['en', 'ru'] as const;
export type PublicLocale = (typeof publicLocales)[number];

export const publicHomeAlternates = publicLocales.map((lang) => ({
  lang,
  href: localeMeta[lang].path,
}));

export const isPublicLocale = (locale: Locale): locale is PublicLocale =>
  publicLocales.includes(locale as PublicLocale);
