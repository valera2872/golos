package com.quietdiary.app;

import android.content.Intent;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import com.google.android.material.button.MaterialButton;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public final class MorningActivity extends AppCompatActivity {
    private TextView title;
    private TextView subtitle;
    private TextView summary;
    private TextView program;
    private TextView reviewProgress;
    private LinearLayout entriesContainer;
    private LinearLayout signsContainer;
    private TextView signsEmpty;

    @Override protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_morning);
        title = findViewById(R.id.morningScreenTitle);
        subtitle = findViewById(R.id.morningScreenSubtitle);
        summary = findViewById(R.id.morningScreenSummary);
        program = findViewById(R.id.morningScreenProgram);
        reviewProgress = findViewById(R.id.morningReviewProgress);
        entriesContainer = findViewById(R.id.morningEntriesContainer);
        signsContainer = findViewById(R.id.morningSignsContainer);
        signsEmpty = findViewById(R.id.morningSignsEmpty);

        findViewById(R.id.morningBackButton).setOnClickListener(v -> finish());
        findViewById(R.id.morningAddDreamButton).setOnClickListener(v ->
                startActivity(new Intent(this, ManualRecordActivity.class)
                        .putExtra(ManualRecordActivity.EXTRA_DREAM, true)));
        findViewById(R.id.morningAllDreamsButton).setOnClickListener(v ->
                startActivity(new Intent(this, DreamHubActivity.class)));
        findViewById(R.id.morningAllNightsButton).setOnClickListener(v ->
                startActivity(new Intent(this, NightArchiveActivity.class)));
    }

    @Override protected void onResume() {
        super.onResume();
        NightSessionStore.syncFromPreferences(this);
        render();
    }

    private void render() {
        MorningTools.Summary data = MorningTools.latestSummary(this);
        if (data.session == null) {
            title.setText("Доброе утро");
            subtitle.setText("После первой ночи Somnori соберёт здесь всё, что вы успели сохранить, не просыпаясь окончательно.");
            summary.setText("Пока нет завершённой ночи");
            program.setVisibility(View.GONE);
            reviewProgress.setText("Ночные сны появятся здесь автоматически.");
            entriesContainer.removeAllViews();
            addEmpty(entriesContainer, "Запустите Ночного помощника перед сном. Утром записи уже будут ждать вас здесь.");
            renderSigns();
            return;
        }

        long end = data.session.effectiveEnd(System.currentTimeMillis());
        title.setText("Доброе утро");
        subtitle.setText("Somnori сохранил ночь · " + dateLabel(data.session.startedAt, end));
        summary.setText(data.dreams + " " + plural(data.dreams, "сон", "сна", "снов")
                + " · " + data.notes + " " + plural(data.notes, "другая запись", "другие записи", "других записей")
                + " · " + data.session.timeRequestCount + " "
                + plural(data.session.timeRequestCount, "запрос времени", "запроса времени", "запросов времени"));

        String programText = programSummary(data.session);
        program.setVisibility(programText.isEmpty() ? View.GONE : View.VISIBLE);
        program.setText(programText.isEmpty() ? "" : "Перед сном · " + programText);

        if (data.dreams == 0) {
            reviewProgress.setText("Если что-то осталось от сна — добавьте это голосом сейчас, пока воспоминание ещё рядом.");
        } else if (data.reviewedDreams >= data.dreams) {
            reviewProgress.setText("Утренний разбор завершён для всех снов этой ночи.");
        } else {
            int left = data.dreams - data.reviewedDreams;
            reviewProgress.setText("Осталось разобрать " + left + " " + plural(left, "сон", "сна", "снов")
                    + " · отметьте яркость, настроение и признаки сна.");
        }

        entriesContainer.removeAllViews();
        if (data.entries.isEmpty()) addEmpty(entriesContainer, "В этой ночи нет сохранённых записей.");
        else for (Entry entry : data.entries) entriesContainer.addView(createEntryCard(entry));
        renderSigns();
    }

    private View createEntryCard(Entry entry) {
        LinearLayout card = new LinearLayout(this);
        card.setOrientation(LinearLayout.VERTICAL);
        card.setPadding(dp(16), dp(15), dp(16), dp(15));
        card.setBackgroundResource(entry.isDream() ? R.drawable.dream_card_background : R.drawable.surface_glass_background);
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(-1, -2);
        params.bottomMargin = dp(10);
        card.setLayoutParams(params);

        TextView meta = new TextView(this);
        meta.setText(time(entry.createdAt) + " · " + (entry.isDream() ? "СОН" : entry.category.toUpperCase(Locale.ROOT)));
        meta.setTextColor(ContextCompat.getColor(this, entry.isDream() ? R.color.qd_dream : R.color.qd_primary));
        meta.setTextSize(10.5f);
        meta.setLetterSpacing(0.05f);
        card.addView(meta);

        TextView titleView = new TextView(this);
        titleView.setText(entry.title == null || entry.title.trim().isEmpty() ? "Ночная запись" : entry.title.trim());
        titleView.setTextColor(ContextCompat.getColor(this, R.color.qd_text));
        titleView.setTextSize(17);
        titleView.setTypeface(titleView.getTypeface(), android.graphics.Typeface.BOLD);
        titleView.setPadding(0, dp(6), 0, 0);
        titleView.setMaxLines(2);
        card.addView(titleView);

        TextView body = new TextView(this);
        String preview = MorningTools.preview(entry, 240);
        body.setText(preview.isEmpty() ? "Расшифровка пока отсутствует" : preview);
        body.setTextColor(ContextCompat.getColor(this, R.color.qd_muted));
        body.setTextSize(13);
        body.setLineSpacing(0f, 1.12f);
        body.setPadding(0, dp(7), 0, 0);
        body.setMaxLines(5);
        card.addView(body);

        if (entry.isDream()) {
            StringBuilder details = new StringBuilder();
            if (entry.dreamRecall > 0) details.append("Яркость ").append(entry.dreamRecall).append("/5");
            if (entry.lucidDream) appendDot(details, "осознанный сон");
            if (entry.dreamMood != null && !entry.dreamMood.trim().isEmpty()) appendDot(details, entry.dreamMood.trim());
            if (entry.dreamSigns != null && !entry.dreamSigns.trim().isEmpty()) appendDot(details, "признаки: " + entry.dreamSigns.trim());
            if (details.length() > 0) {
                TextView info = new TextView(this);
                info.setText(details.toString());
                info.setTextColor(ContextCompat.getColor(this, R.color.qd_dream));
                info.setTextSize(11.5f);
                info.setPadding(0, dp(9), 0, 0);
                info.setMaxLines(3);
                card.addView(info);
            }
        }

        MaterialButton open = new MaterialButton(this);
        open.setAllCaps(false);
        open.setText(entry.isDream() && !entry.dreamReviewed ? "Разобрать сон" : "Открыть запись");
        open.setTextSize(11);
        open.setCornerRadius(dp(18));
        open.setTextColor(ContextCompat.getColor(this, R.color.qd_primary_dark));
        open.setBackgroundTintList(android.content.res.ColorStateList.valueOf(
                ContextCompat.getColor(this, entry.isDream() ? R.color.qd_dream : R.color.qd_primary)));
        open.setOnClickListener(v -> startActivity(new Intent(this, EntryDetailActivity.class)
                .putExtra(EntryDetailActivity.EXTRA_ENTRY_ID, entry.createdAt)));
        LinearLayout.LayoutParams buttonParams = new LinearLayout.LayoutParams(-1, dp(46));
        buttonParams.topMargin = dp(12);
        card.addView(open, buttonParams);
        card.setOnClickListener(v -> open.performClick());
        return card;
    }

    private void renderSigns() {
        signsContainer.removeAllViews();
        List<DreamTools.SignStat> signs = MorningTools.repeatedSigns(this, 5);
        signsEmpty.setVisibility(signs.isEmpty() ? View.VISIBLE : View.GONE);
        for (DreamTools.SignStat stat : signs) {
            LinearLayout row = new LinearLayout(this);
            row.setOrientation(LinearLayout.HORIZONTAL);
            row.setGravity(Gravity.CENTER_VERTICAL);
            row.setPadding(dp(13), dp(11), dp(13), dp(11));
            row.setBackgroundResource(R.drawable.metric_background);
            LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(-1, -2);
            params.bottomMargin = dp(7);
            row.setLayoutParams(params);

            TextView label = new TextView(this);
            label.setText(stat.label);
            label.setTextColor(ContextCompat.getColor(this, R.color.qd_text));
            label.setTextSize(13);
            label.setTypeface(label.getTypeface(), android.graphics.Typeface.BOLD);
            row.addView(label, new LinearLayout.LayoutParams(0, -2, 1f));

            TextView count = new TextView(this);
            count.setText(stat.count + "×");
            count.setTextColor(ContextCompat.getColor(this, R.color.qd_dream));
            count.setTextSize(13);
            count.setTypeface(count.getTypeface(), android.graphics.Typeface.BOLD);
            row.addView(count);
            signsContainer.addView(row);
        }
    }

    private void addEmpty(LinearLayout container, String text) {
        TextView empty = new TextView(this);
        empty.setText(text);
        empty.setTextColor(ContextCompat.getColor(this, R.color.qd_muted));
        empty.setTextSize(13);
        empty.setLineSpacing(0f, 1.12f);
        empty.setPadding(dp(4), dp(12), dp(4), dp(12));
        container.addView(empty);
    }

    private String programSummary(NightSession session) {
        String p = session.practice == null ? "" : session.practice.trim();
        String a = session.audioProgram == null ? "" : session.audioProgram.trim();
        if (!p.isEmpty() && !a.isEmpty()) return p + " → " + a;
        return !p.isEmpty() ? p : a;
    }

    private String dateLabel(long start, long end) {
        SimpleDateFormat day = new SimpleDateFormat("d MMMM", Locale.getDefault());
        String a = day.format(new Date(start));
        String b = day.format(new Date(end));
        return a.equals(b) ? a : a + " → " + b;
    }

    private String time(long millis) {
        return new SimpleDateFormat("HH:mm", Locale.getDefault()).format(new Date(millis));
    }

    private static void appendDot(StringBuilder out, String value) {
        if (out.length() > 0) out.append(" · ");
        out.append(value);
    }

    private String plural(int count, String one, String few, String many) {
        int mod100 = Math.abs(count) % 100;
        int mod10 = Math.abs(count) % 10;
        if (mod100 >= 11 && mod100 <= 14) return many;
        if (mod10 == 1) return one;
        if (mod10 >= 2 && mod10 <= 4) return few;
        return many;
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }
}
