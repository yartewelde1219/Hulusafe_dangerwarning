# Annotation guidelines

Annotate Amharic news only from explicitly stated information.

- `danger`: yes/no
- `danger_type`: conflict, flood, fire, landslide, drought, earthquake, extreme_weather, other
- `location`: region/zone/woreda/city as written, or Unknown
- `event_time`: date if stated, else Unknown
- `publication_time`: source timestamp
- `deaths`, `injuries`, `displaced`, `missing`, `damage`: number/text only if stated; otherwise Unknown
- `negated`, `historical`, `hypothetical`, `current_active`: yes/no

Do not estimate casualties. `0` means the article stated zero. Unknown is not zero.

Recommended tool: Label Studio. Export JSONL into `ai/dataset/`.
