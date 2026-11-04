# دليل Power BI — تحليل أسعار المنازل (Ames, Iowa)

هالدليل يخليك تعيد بناء نفس الداشبورد في **Power BI Desktop** على لابتوبك خلال ~15 دقيقة.
الصورة المرجعية للشكل النهائي المطلوب: `dashboard.png` الموجودة في نفس المجلد — افتحها جنبك وطبق عليها.

> **المتطلب المسبق:** ثبّت Python على جهازك مع مكتبتي `pandas` و `matplotlib`
> (`pip install pandas matplotlib`)، وفعّله في Power BI من
> **File ← Options and settings ← Options ← Python scripting**.

## الطريق الأسرع: فيجوال بايثون (صفحتين جاهزتين)

### الصفحة 1 — نظرة عامة (Overview)
1. **Get Data** ← حمّل `data/ames_housing.csv`.
2. أنشئ صفحة جديدة وسمّها **Overview**، ومن **Insert** أضف **Python visual**.
3. اسحب إلى خانة **Values** في الفيجوال هذه الأعمدة الثلاثة بالضبط:
   `SalePrice` ← `GrLivArea` ← `OverallQual`.
4. الصق كامل محتوى الملف `powerbi-page1-overview.py` في محرر السكربت ← اضغط Run.

### الصفحة 2 — التفاصيل (Details)
1. أنشئ صفحة ثانية وسمّها **Details**، وأضف **Python visual** جديد.
2. اسحب إلى خانة **Values** هذه الأعمدة الأربعة بالضبط:
   `SalePrice` ← `Neighborhood` ← `YearBuilt` ← `OverallQual`.
3. الصق كامل محتوى الملف `powerbi-page2-details.py` ← اضغط Run.

### إضافة Slicers (فلاتر تفاعلية)
أضف Slicers عادية من قائمة الـ Visualizations وستعمل تلقائياً على فيجوال بايثون:
- **Slicer** ← `Neighborhood` | **Slicer** ← `OverallQual` | **Slicer** ← `YearBuilt` (نطاق).

> **ملاحظة صادقة:** الـ Slicers **تُرشّح** فيجوال بايثون فعلاً — الصفوف المفلترة هي اللي توصل
> لمتغير `dataset` داخل السكربت، ففلاترك شغالة. لكن فيجوال بايثون **لا يستقبل** التظليل
> التفاعلي (highlight) من الضغط على رسوم بيانية ثانية — الفلترة بالـ Slicers شغالة،
> التفاعل بالنقر على الأعمدة لا.

---
## الطريق الثاني: بناء يدوي بمقاييس DAX (اختياري)

## 1) تحميل البيانات (Get Data)

1. افتح Power BI Desktop ← من الشريط العلوي **Home** ← **Get Data** ← **Text/CSV**.
2. اختر الملف: `data/ames_housing.csv` (1,460 صف × 80 عمود).
3. اضغط **Load**.

> جدول واحد فقط — ما تحتاج علاقات (Relationships) لأن كل البيانات في جدول واحد اسمه `ames_housing`.

## 2) تنظيف سريع في Power Query (اختياري لكن مفضل)

1. من **Home** ← **Transform Data** لفتح Power Query.
2. عمود `Id` محذوف أصلاً من الملف. تأكد من أنواع الأعمدة:
   - `SalePrice` و `GrLivArea` و `YearBuilt` ← نوع **Whole Number**.
   - `Neighborhood` و `OverallQual` ← نوع **Text** (OverallQual خله Text عشان يظهر كفئات 1-10).
3. أضف عمود العقد (Decade) — من تبويب **Add Column** ← **Custom Column**:
   - الاسم: `Decade`
   - الصيغة (لغة M):
     ```
     Number.RoundDown([YearBuilt] / 10) * 10
     ```
4. اضغط **Close & Apply**.

## 3) مقاييس DAX (انسخ والصق)

من تبويب **Table tools** ← **New measure**، وأنشئ هالمقاييس الأربعة (انسخها زي ما هي):

```dax
Median Sale Price = MEDIAN(ames_housing[SalePrice])
```

```dax
Mean Sale Price = AVERAGE(ames_housing[SalePrice])
```

```dax
Transactions = COUNTROWS(ames_housing)
```

```dax
Avg Price per Sqft = AVERAGEX(ames_housing, DIVIDE(ames_housing[SalePrice], ames_housing[GrLivArea]))
```

> ملاحظة: `DIVIDE` تحميك من القسمة على صفر لو فيه صف `GrLivArea` بصفر.

## 4) بناء الصفحة — المرئيات (Visuals)

رتبها زي `dashboard.png`: صف علوي للـ KPIs، وتحته الرسوم.

**صف الـ KPIs (أربع بطاقات Card):**
- أضف 4 visuals من نوع **Card** وضع فيها بالترتيب: `Median Sale Price` ← `Mean Sale Price` ← `Transactions` ← `Avg Price per Sqft`.
- من **Format** ← **Callout value** ← فعّل **Display units** = None عشان يطلع الرقم كامل.

**1. توزيع أسعار البيع (Sale Price Distribution):**
- Visual: **Clustered column chart**.
- في Power BI ما فيه Histogram جاهز: كليك يمين على حقل `SalePrice` في الـ Fields ← **New group** ← نوع **Bin** ← حجم الـ Bin = `25000` ← OK (ينشئ حقل `SalePrice (bins)`).
- ضع `SalePrice (bins)` في **X-axis** و `Transactions` (أو Count of SalePrice) في **Y-axis**.

**2. مساحة المعيشة مقابل السعر (Scatter):**
- Visual: **Scatter chart**.
- **X-axis** ← `GrLivArea` | **Y-axis** ← `SalePrice` | **Legend** ← `OverallQual`.

**3. أغلى 10 أحياء (Top 10 Neighborhoods):**
- Visual: **Bar chart** (أفقي).
- **Y-axis** ← `Neighborhood` | **X-axis** ← حقل `SalePrice` (غيّر التجميع إلى **Median** من السهم جنب الحقل).
- من **Filters on this visual** ← `Neighborhood` ← **Filter type** = Top N ← Top = `10` ← By value = Median of SalePrice.

**4. متوسط السعر حسب العقد (Decade):**
- Visual: **Clustered column chart**.
- **X-axis** ← `Decade` | **Y-axis** ← `SalePrice` بتجميع **Median**.

**5. السعر حسب جودة التشطيب (Boxplot):**
- الـ Boxplot مو موجود افتراضياً: من **Visualizations** ← **...** ← **Get more visuals** ← ابحث عن **"Box and Whisker chart by MAQ Software"** ← أضفه.
- **Category** ← `OverallQual` | **Values** ← `SalePrice`.

**الفلاتر (Slicers) — حطها على جنب الصفحة:**
- **Slicer** ← `Neighborhood` (قائمة)
- **Slicer** ← `OverallQual` (قائمة)
- **Slicer** ← `YearBuilt` (من نوع Range/نطاق)

## 5) اللمسات الأخيرة

1. عنوان الصفحة: **Ames, Iowa Housing Price Analytics**.
2. من **View** ← **Themes** اختر ثيم داكن أو فاتح زي ما يعجبك (الصورة المرجعية فاتحة).
3. احفظ الملف: **File** ← **Save** بصيغة `.pbix`.

## أرقام للمقارنة (من البيانات الحقيقية)

بعد ما تبني الداشبورد، قارن أرقامك بهذي عشان تتأكد إن كل شي صح:
- عدد الصفقات (Transactions) = **1,460**.
- الوسيط (Median Sale Price) = **$163,000** والمتوسط (Mean) = **$180,921**.
- العلاقة بين `GrLivArea` و `SalePrice` قوية وموجبة (r ≈ 0.71).
- أغلى حي بالوسيط هو **NridgHt**.

بالتوفيق! 🚀
