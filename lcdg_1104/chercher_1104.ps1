# Planches de candidats pour les plans faibles des reels du 04/11/2026 (pas de visage, pas de decor d'epoque)
Set-Location "C:\Users\NR SMART\tools\lcdg-reel"
$py = ".venv\Scripts\python.exe"
$jobs = @(
  @("2026-11-04-soins-pharmacien", 0, "pharmacy shelves medicine boxes", "pharmacist hands giving medicine box", "green cross pharmacy sign"),
  @("2026-11-04-soins-pharmacien", 1, "pharmacist hands medicine counter", "pharmacy drugstore shelves modern", "hand taking medicine box shelf"),
  @("2026-11-04-soins-pharmacien", 2, "hands typing laptop stethoscope", "doctor hands keyboard computer", "typing laptop desk daylight"),
  @("2026-11-04-soins-pharmacien", 3, "doctor hands reading paper", "medical report hands desk", "reading documents hands stethoscope"),
  @("2026-11-04-soins-pharmacien", 5, "stethoscope desk daylight", "stethoscope laptop desk", "stethoscope notebook top view"),
  @("2026-11-04-soins-pharmacien", 8, "hands on computer mouse office", "doctor typing computer hands", "email inbox laptop hands"),
  @("2026-11-04-soins-pharmacien", 10, "hands smartphone daylight", "woman hands phone sofa bright", "smartphone hand close up bright"),
  @("2026-11-04-soins-pharmacien", 11, "euro coins table bright", "coins stack white background", "money coins hand daylight"),
  @("2026-11-04-soins-pharmacien", 12, "stethoscope desk top view", "doctor office desk empty daylight", "medical desk notebook stethoscope"),
  @("2026-11-04-cotisation-ordre", 1, "opening letter envelope hands", "reading letter hands table", "mail envelope hands desk"),
  @("2026-11-04-cotisation-ordre", 2, "business partners signing document hands", "doctors hands meeting table", "team hands table documents"),
  @("2026-11-04-cotisation-ordre", 6, "binders folders office shelf bright", "stack of documents office", "files paperwork desk daylight"),
  @("2026-11-04-cotisation-ordre", 9, "notebook pen desk daylight", "writing notes hands desk bright", "stethoscope paperwork desk"),
  @("2026-11-04-premieres-installations", 2, "stethoscope doctor office bright", "doctor hands desk stethoscope daylight", "medical office desk bright"),
  @("2026-11-04-premieres-installations", 3, "rural village aerial france", "small town main street daylight", "countryside village road"),
  @("2026-11-04-premieres-installations", 4, "doctor walking corridor from behind", "doctor white coat back view hallway", "hospital corridor walking back"),
  @("2026-11-04-premieres-installations", 5, "blood pressure senior patient hands", "doctor hands holding patient hands", "elderly patient doctor hands daylight"),
  @("2026-11-04-premieres-installations", 6, "empty waiting room", "medical waiting room chairs", "clinic reception empty daylight"),
  @("2026-11-04-premieres-installations", 7, "stethoscope window light", "empty doctor office window", "doctor office chair empty daylight"),
  @("2026-11-04-premieres-installations", 10, "doctor desk stethoscope laptop daylight", "doctor writing notes hands", "medical notes pen hand")
)
foreach ($j in $jobs) {
  $ep, $b, $req = $j[0], $j[1], $j[2..($j.Length - 1)]
  Write-Output "== $ep B$b"
  & $py scripts/broll.py chercher "episodes/$ep" $b --mixte @req 2>&1 | Select-Object -Last 1
}
