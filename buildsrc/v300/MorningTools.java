package com.quietdiary.app;

import android.content.Context;

import java.util.ArrayList;
import java.util.List;

/** Read-only helpers for the morning experience. No recognition code depends on this class. */
public final class MorningTools {
    public static final class Summary {
        public final NightSession session;
        public final List<Entry> entries;
        public final int dreams;
        public final int notes;
        public final int reviewedDreams;

        Summary(NightSession session, List<Entry> entries, int dreams, int notes, int reviewedDreams) {
            this.session = session;
            this.entries = entries;
            this.dreams = dreams;
            this.notes = notes;
            this.reviewedDreams = reviewedDreams;
        }
    }

    private MorningTools() {}

    public static NightSession latestCompletedNight(Context context) {
        NightSession fallback = null;
        for (NightSession session : NightSessionStore.loadAll(context)) {
            if (fallback == null) fallback = session;
            if (!session.isActive()) return session;
        }
        return fallback;
    }

    public static Summary latestSummary(Context context) {
        NightSession session = latestCompletedNight(context);
        List<Entry> entries = session == null ? new ArrayList<>() : NightSessionStore.entries(context, session);
        int dreams = 0;
        int reviewed = 0;
        for (Entry entry : entries) {
            if (entry.isDream()) {
                dreams++;
                if (entry.dreamReviewed) reviewed++;
            }
        }
        return new Summary(session, entries, dreams, Math.max(0, entries.size() - dreams), reviewed);
    }

    public static List<DreamTools.SignStat> repeatedSigns(Context context, int limit) {
        List<DreamTools.SignStat> result = new ArrayList<>();
        for (DreamTools.SignStat stat : DreamTools.aggregateSigns(EntryStore.loadDreams(context))) {
            if (stat.count < 2) continue;
            result.add(stat);
            if (result.size() >= Math.max(1, limit)) break;
        }
        return result;
    }

    public static String preview(Entry entry, int maxChars) {
        if (entry == null || entry.transcript == null) return "";
        String text = entry.transcript.trim().replaceAll("\\s+", " ");
        int limit = Math.max(20, maxChars);
        return text.length() <= limit ? text : text.substring(0, Math.max(1, limit - 1)).trim() + "…";
    }
}
