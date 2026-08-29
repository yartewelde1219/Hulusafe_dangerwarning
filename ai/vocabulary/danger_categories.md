# Danger Vocabulary & Category Mapping

This document details the Amharic vocabulary, category classifications, and scoring indicators utilized by the HuluSafe NLP pipeline (Student 4) and Danger Intelligence Engine (Student 5).

---

## 1. Danger Categories & Amharic Keywords

### CONFLICT (ግጭት / ጦርነት)
- **Primary Keywords**: ግጭት, ጦርነት, ውጊያ, ታጣቂ, ታጣቂዎች, ጥቃት, ጥይት, መተኮስ, የጸጥታ ችግር, ታጣቂ ቡድኖች
- **Casualty Indicators**: ተገደሉ, ሞቱ, ቆሰሉ, ተፈናቀሉ, ታገቱ
- **Baseline Weight**: 0.90 (High severity)

### FLOOD (ጎርፍ)
- **Primary Keywords**: ጎርፍ, የጎርፍ አደጋ, የወንዝ ሙላት, መጥለቅለቅ, ውሃ ሞላ, ተጥለቀለቀ
- **Impact Indicators**: ቤቶች ፈረሱ, ቤቶች ወድመዋል, ድልድይ ተሰበረ, ሰብል ወደመ, ተፈናቀሉ
- **Baseline Weight**: 0.75

### FIRE (እሳት / ቃጠሎ)
- **Primary Keywords**: እሳት, የእሳት አደጋ, ቃጠሎ, ተቃጠለ, የደን ቃጠሎ, ነበልባል
- **Impact Indicators**: ሱቆች ተቃጠሉ, ንብረት ወደመ, መኖሪያ ቤቶች ተቃጠሉ
- **Baseline Weight**: 0.70

### LANDSLIDE (የመሬት መንሸራተት / ናዳ)
- **Primary Keywords**: የመሬት መንሸራተት, የመሬት ናዳ, ተራራ ተደርምሶ, ናዳ, መደርመስ
- **Impact Indicators**: ተቀበሩ, ቤቶች ተደረመሱ, መንገድ ተዘጋ, ተቀብረው የሞቱ
- **Baseline Weight**: 0.85

### DROUGHT (ድርቅ)
- **Primary Keywords**: ድርቅ, የዝናብ እጥረት, የውሃ እጥረት, ረሀብ, የምግብ እጥረት, ከብቶች ሞቱ
- **Impact Indicators**: የእርዳታ እጥረት, ረሀብ ተከሰተ, የተራቡ ዜጎች
- **Baseline Weight**: 0.65

### EARTHQUAKE (የመሬት መንቀጥቀጥ)
- **Primary Keywords**: የመሬት መንቀጥቀጥ, ርዕደ መሬት, መንቀጥቀጥ, የሬክተር ስኬል
- **Impact Indicators**: ህንፃዎች ፈረሱ, ስንጥቅ, ተናወጠ
- **Baseline Weight**: 0.80

### EXTREME WEATHER (ከባድ የአየር ሁኔታ)
- **Primary Keywords**: ከባድ ዝናብ, የበረዶ ዝናብ, አውሎ ንፋስ, ውርጭ, ማዕበል
- **Impact Indicators**: ጣሪያ ተገነጠለ, የኤሌክትሪክ መስመር ተቋረጠ, ዛፎች ወደቁ
- **Baseline Weight**: 0.60

### OTHER (ሌሎች ድንገተኛ አደጋዎች)
- **Primary Keywords**: የትራፊክ አደጋ, የመኪና አደጋ, የጀልባ መስመጥ, ወረርሽኝ, ህመም
- **Baseline Weight**: 0.50

### NORMAL (መደበኛ ዜና / አደጋ የሌለበት)
- **Primary Keywords**: ሰላም, ልማት, ምርቃት, ስፖርት, ንግድ, ኢኮኖሚ, ትምህርት, የአየር ሁኔታው መደበኛ ነው
- **Baseline Weight**: 0.00

---

## 2. Context & Negation Markers

- **Negation Markers (አሉታዊ)**: `የለም`, `አይደለም`, `አልተከሰተም`, `የለምም`, `አልደረሰም`, `አልተነሳም`, `አልተገኘም`
- **Historical Markers (ታሪካዊ)**: `በፊት`, `ባለፈው`, `ከዓመታት በፊት`, `ባለፈው ዓመት`, `ታሪክ`, `የነበረው`, `እንደነበር`
- **Hypothetical Markers (ግምታዊ / ወደፊት)**: `ቢሆን`, `ሊከሰት ይችላል`, `ከተከሰተ`, `ተብሎ ተሰግቷል`, `ሊያስከትል ይችላል`

---

## 3. Severity & Impact Weighting Formula

Combined severity score:
$$\text{Severity} = 0.25 \times \text{Impact} + 0.20 \times \text{NLP Evidence} + 0.20 \times \text{Source Credibility} + 0.20 \times \text{Agreement} + 0.10 \times \text{Recency} + 0.05 \times \text{Location Confidence}$$

