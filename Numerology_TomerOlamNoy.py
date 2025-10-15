# ====================================================
# Numerology_TomerOlamNoy.py - קוד מלא ומתוקן סופית
# ====================================================
import streamlit as st
import pandas as pd
from datetime import datetime
import re

# 1. קבועים גלובליים והגדרות
# ----------------------------------------------
MASTER_NUMBERS = {11, 22}
ALL_MASTER_NUMBERS = {11, 22, 33} 
KARMIC_NUMBERS = {13, 14, 16, 19}
SPECIAL_NUMBERS = ALL_MASTER_NUMBERS.union(KARMIC_NUMBERS)

ASTRO_MAP = {
    'גדי': 8, 'דלי': 11, 'דגים': 7, 'טלה': 9, 'שור': 33, 'תאומים': 5,
    'מאזניים': 6, 'סרטן': 2, 'אריה': 1, 'בתולה': 4, 'עקרב': 22, 'קשת': 3
}

GIMATRIA_MAP = {
    'א': 1, 'ה': 5, 'ו': 6, 'י': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ז': 7, 'ח': 8, 
    'ט': 9, 'כ': 2, 'ל': 3, 'מ': 4, 'נ': 5, 'ס': 6, 'ע': 7, 'פ': 8, 'צ': 9, 
    'ק': 1, 'ר': 2, 'ש': 3, 'ת': 4, 
    'ץ': 9, 'ף': 8, 'ם': 4, 'ך': 2, 'ן': 5 
}
VOWEL_LETTERS = {'א', 'ה', 'ו', 'י'}
CONSONANTS = set(GIMATRIA_MAP.keys()) - VOWEL_LETTERS 
VOWELS_MAP = {k: GIMATRIA_MAP[k] for k in VOWEL_LETTERS}

# מפת טקסט עוצמות
STRENGTH_TEXT_MAP = {
    'MASTER': '⭐ תדר מאסטר חזק',
    'STRONG': '✅ תדר חזק ומקדם',
    'MEDIUM': '➖ תדר מאוזן',
    'WEAK': '⚠️ תדר חלש/מעכב',
    'KARMIC': '❌ תדר קארמתי - היזהר',
    'NEUTRAL': '➖ תדר מאוזן (ברירת מחדל)'
}

# 🚨 משפט הקארמה המבוקש
KARMIC_WARNING = "נטייה לחשיבה ראשונה שלילית. רצוי לקבל החלטות רק לאחר שנרגעים ולהתייחס לחשיבה השנייה ולא לראשונה."

# 🚨 מפות הניתוח המרוכזות - המפתחות תוקנו לשמות התדרים החדשים
CHAKRA_ANALYSIS = {
    # הותאם מ'צ'אקרת הבסיס'
    'תדר סביבתי': { 
        1: "הסביבה תופסת את האדם כמוביל טבעי וכדמות סוחפת.",
        2: "הסביבה תופסת את האדם כדמות משפחתית המחפשת זוגיות ויציבות רגשית.",
        3: "הסביבה רואה את האדם כחובב חברה, שמחה, טיולים ובעל אנרגיה קלילה.",
        4: "הסביבה רואה את האדם כמי שמעריך מסגרת, יציבות ובסיס בטוח.",
        5: "הסביבה רואה את האדם כתקשורתי ביותר ובעל יכולת ביטוי גבוהה.",
        6: "הסביבה תופסת אותו כדמות משפחתית ובעלת נתינה גבוהה, לעיתים עד כדי ביטול עצמי וריצוי יתר.",
        7: "בחוויה הפנימית מרגיש שונה (דומה ל-16). בחברה הוא נוטה להיות שקט יותר, אוהב להקשיב, לצפות ולנתח התנהגויות. אוהב לצבור ידע.",
        8: "הסביבה תופסת את האדם כחזק, בעל יכולות ניהוליות גבוהות ומחפש איזון בין רוחניות לגשמיות.",
        9: "הסביבה רואה פוטנציאל גבוה ובלתי ממומש. אדם שנולד להוביל דרך.",
        11: "הסביבה תופסת את האדם כבעל פוטנציאל גדול, אך הוא עלול להתקשות לממשו.",
        13: f"הסביבה רואה אותו כנוקשה, קשה וביקורתי. מתקשה בזוגיות ואוהב שדברים נעשים אך ורק בדרך שלו. {KARMIC_WARNING}",
        14: f"מאופיין בקושי במערכות יחסים זוגיות (דחף לפרקן) ובנטייה לבזבזנות. 'מה שהאדם מרוויח, הכסף יורד לטמיון'. {KARMIC_WARNING}",
        16: f"אדם עם נטייה להפסדים כספיים ובעיות בזוגיות. בחוויה הפנימית מרגיש שונה ועם עיכובים קשים במימוש. {KARMIC_WARNING}",
        19: f"מאופיין בהרגשת קורבנות. מפה חלשה: חווה קורבן. מפה חזקה: נוטה למקרבן בזוגיות. {KARMIC_WARNING}",
        22: "הסביבה רואה אדם כריזמטי, אהוב ומוביל, אבל שמתקשה לממש את הפוטנציאל שלו."
    },
    # הותאם מ'צ'אקרת העל'
    'תדר השם': { 
        1: "תדר אנרגטי חיובי המקדם את האדם מבחינה אנרגטית.",
        2: "אין השפעה אנרגטית משמעותית על המפה.",
        3: "תדר אנרגטי טוב המקדם את האדם.",
        4: "אין השפעה אנרגטית משמעותית על המפה.",
        5: "תדר אנרגטי טוב המקדם תקשורת. תדר אנרגטי טוב המקדם את האדם.",
        6: "אין השפעה אנרגטית משמעותית על המפה.",
        7: "עלול לגרום לעיכובים קלים ולבעיות נפשיות קלות.",
        8: "תדר אנרגטי טוב המקדם את האדם.",
        9: "תדר אנרגטי טוב המקדם את האדם.",
        11: "תדר אנרגטי טוב המקדם את האדם.",
        13: f"ערך קארמתי המצביע על נוקשות של האדם. {KARMIC_WARNING} | הסביבה רואה אותו כנוקשה, קשה וביקורתי. מתקשה בזוגיות ואוהב שדברים נעשים אך ורק בדרך שלו.",
        14: f"ערך קארמתי. {KARMIC_WARNING} | מאופיין בקושי במערכות יחסים זוגיות (דחף לפרקן) ובנטייה לבזבזנות. 'מה שהאדם מרוויח, הכסף יורד לטמיון'.",
        16: f"ערך קארמתי. {KARMIC_WARNING} | אדם עם נטייה להפסדים כספיים ובעיות בזוגיות. בחוויה הפנימית מרגיש שונה ועם עיכובים קשים במימוש.",
        19: f"ערך קארמתי. {KARMIC_WARNING} | מאופיין בהרגשת קורבנות. מפה חלשה: חווה קורבן. מפה חזקה: נוטה למקרבן בזוגיות.",
        22: "תדר אנרגטי טוב המקדם את האדם."
    },
    # הותאם מ'צ'אקרת המין והיצירה'
    'תדר תעסוקה': { 
        1: "יכולות תעסוקה מעולות: הצלחה מרובה כמנהיג, מנהל/סמנכ\"ל או עצמאי בכל תחום (כולל עבודת כפיים). אנרגיה חזקה שדוחפת להצלחה ללא תנאי.",
        2: "מתאים לעבודה במתן שירות (פקידות, הוראה, טיפול). נטייה להיות שכיר וקושי בהשגת משכורות גבוהות.",
        3: "כישורי תעסוקה מצוינים, מתאים לעבודה על במה, הוראה, מכירות, תקשורת, מחשבים, ספורט ומוזיקה. מסוגל לעבוד בכל תחום.",
        4: "יכולות תעסוקה בינוניות, מתאים למתן שירות כשכיר. מוטיבציה תעסוקתית לא גבוהה.",
        5: "כישורי תעסוקה ייחודיים ומצוינים בתחומים כמו ספורט, מוזיקה, מחשבים וראיית חשבון. יכולת להגיע לתפקידים בכירים ופוטנציאל גבוה לרווחים.",
        6: "כמו יכולות 4: מתאים יותר למתן שירות כשכיר.",
        7: "כישורי תעסוקה קשים ליישום (הוראה, רפואה, הייטק). רובם עובדים במתן שירות ומתקשים לממש את הפוטנציאל הגבוה.",
        8: "יכולות תעסוקה הטובות בעולם, מתאימות לניהול אנשים, עסקים מצליחים, ייעוץ השקעות, ביטוח ועו\"ד. נמנעים מעבודת כפיים, בעלי יכולת להתמודד עם קהל גדול.",
        9: "יכולות תעסוקה בינוניות. סיכוי נמוך למימוש מלוא הפוטנציאל. נוטה לעבוד במתן שירות (כמו 2, 4, 6).",
        11: "כמו יכולות 9: נוטה לעבוד במתן שירות ומתקשה לממש פוטנציאל.",
        13: f"יוצר קושי, חוסר סיפוק וקושי במימוש הפוטנציאל. לרוב יהיה שכיר. {KARMIC_WARNING}",
        14: f"כמו יכולות 13. ייחודי בכך שיכול להצטיין גם בתחומי ספורט ומוזיקה. {KARMIC_WARNING}",
        16: f"כמו יכולות 13. יוצר קושי, חוסר סיפוק וקושי במימוש הפוטנציאל. לרוב יהיה שכיר. {KARMIC_WARNING}",
        19: f"מצד אחד יכולות מצוינות (19=1), אך יש קושי להגיע ליכולות של 1. רעיונות מצוינים, קושי גדול ביישום. מצליח לממש עד 70% מהפוטנציאל. נטייה לדברים להשתבש, מוטיבציה גבוהה אך יישום בינוני. {KARMIC_WARNING}",
        22: "כמו יכולות 9: נוטה לעבוד במתן שירות ומתקשה לממש פוטנציאל.",
        33: "כמו יכולות 6/4: נוטה לעבוד במתן שירות ומתקשה לממש פוטנציאל."
    },
    # הותאם מ'צ'אקרת מקלעת השמש'
    'תדר הייעוד': { 
        1: "הייעוד הוא להנהיג: להיות לידר, לעמוד על במה, להעביר ידע, להיות עצמאי. אנרגיה מובילה וחזקה המקלה על הצלחה.",
        2: "הייעוד הוא שיתוף פעולה: להיות איש משפחה, לעבוד בצוותים ולטפל. נטייה לרגשנות וחרדות (הצורך בפעולה משותפת).",
        3: "הייעוד הוא קלילות ושמחה: לשמור על הילד הפנימי, לטייל, לבלות בחברה, לעמוד על במה ולהיות שמח. משיכה לספורט, מוזיקה ואסתטיקה.",
        4: "הייעוד הוא יציבות ומסגרת: להיות אדם מסודר ומאורגן שחי במסגרות; אדם משפחתי עם בסיס חזק.",
        5: "הייעוד הוא תקשורת וגבולות: לעמוד על במה, להעביר ידע, תקשורת, מדיה, מחשבים וראיית חשבון. קל להצליח בחיים.",
        6: "הייעוד הוא נתינה ומשפחה: להיות 'מלך המשפחה' ולשרת את הסביבה. נטייה לתחומי אסתטיקה וטיפול. קיים קושי בקבלת עזרה (נטייה לריצוי). קל למימוש.",
        7: "הייעוד הוא התחברות עצמית וידע: להתגבר על חרדות ולחצים, לצבור ידע ולהתחבר לרוחניות. נטייה לפעול מהרגש ולא מהשכל (מומלץ להתנהל שכלית). הייעוד המשני הוא לעמוד על במה כ'חכם' או 'נבדל'.",
        8: "הייעוד הוא איזון וניהול: להיות מנהל, עצמאי עשיר ולפרנס משפחה, תוך איזון בין רוחניות לגשמיות. קשה מאוד למימוש (נדיר). הייעוד המשני הוא העברת ידע.",
        9: "ייעוד מאסטר (הגבוה ביותר): להוביל דרך רוחנית/עולמית, להמציא דברים למען האנושות ולטפל בסביבה. נולד למען אחרים. נדרשת מפה חזקה למימוש.",
        11: "ייעוד מאסטר (המטפל הגדול): המסע שלהם הוא להפוך ממטופל ותלותי לאדם חזק שמטפל באנשים. צריכים מפה חזקה כדי להגשים את ייעוד המאסטר.",
        13: f"הייעוד הוא תיקון קרמתי: להשתחרר ממוגבלות (פיזית/נפשית/מנטלית), מנוקשות, חשיבה שלילית וביקורתיות. למצוא שלווה וחופש. {KARMIC_WARNING}",
        14: f"הייעוד הוא תיקון קרמתי: להשתחרר מדחף בלתי נשלט לחופש מוחלט, לפתח יציבות משפחתית וכלכלית. נטייה לבזבזנות, לקיחת סיכונים והשתעממות. {KARMIC_WARNING}",
        16: f"הייעוד המאתגר ביותר (קארמה רוחנית): טיפול בנפש, התגברות על חרדות, קריסות נפשיות ודיכאון. התיקון הוא חיבור לרוחניות, נתינה, וטיפול באחרים (רפואה, פסיכולוגיה). {KARMIC_WARNING}",
        19: f"הייעוד הוא תיקון קרמתי: להשתחרר מקורבנות וללמוד להיות המנהל (לא הסגן). לרוב חווים ניצול משמעותי בשיא הראשון של החיים. {KARMIC_WARNING}",
        22: "דומה לערך 4, פוטנציאל מאסטר.",
        33: "הייעוד להיות איש משפחה, להשתחרר מרצון לשליטה במשפחה ובבני זוג, להתעסק ברוחניות, כתיבה ויצירה."
    },
    # הותאם מ'צ'אקרת הלב'
    'תדר החוסר': { 
        0: "צ'אקרת הלב: במצב מאוזן או במצוקה קארמתית. 0 במינוס (עם קארמה): רצון לקבל ריפוי, נמצא במצוקה וחוסר שביעות רצון פנימית. 0 בפלוס (עם מאסטר): רצון לתת ריפוי, מפה מאוזנת.",
        1: "תחושת חוסר במנהיגות; רצון להוביל יותר. לפעמים מתנהל מאגו.",
        2: "תחושה של חוסר בזוגיות ובמשפחתיות.",
        3: "תחושה של חוסר חופש, קלילות ושמחת חיים.",
        4: "תחושה של רצון מוגבר למסגרתיות, יציבות וסדר.",
        5: "תחושה של חוסר בתקשורת; רצון להיות יותר תקשורתי.",
        6: "תחושה של חוסר במשפחתיות ובאיזון נתינה-קבלה.",
        7: "תחושה של חוסר בידע; רצון ללמוד ולצבור ידע.",
        8: "תחושה של חוסר ביכולות ניהול; צורך באיזון בין הרוחניות לגשמיות ולחזק את יכולות הניהול."
    },
    # הותאם מ'צ'אקרת הגרון'
    'תדר הביטוי והחשיבה': { 
        0: "אם בפלוס: רצון לרפא את העולם. אם במינוס: רצון לקבל ריפוי. דומה לאנרגיה של 2: קשיים בזוגיות, קושי להיות עצמאי ומצליח לבד.",
        1: "יכולות חשיבה מעולות (ציון 100): חשיבה אנרגטית, שכלתנית ולוגית. 'מלך ברעיונות', יכולת עיבוד נתונים גבוהה, מתאים לתפקידי ניהול ועצמאות.",
        2: "חשיבה מצוינת כשכיר, חלשה כעצמאי. מקשה על זוגיות (חשיבה תלותית). טוב בלימודים.",
        3: "חשיבה טובות, 'מלך ביצירתיות'. סגנון חשיבה מהיר אך קושי בהתמדה (בעיקר בזוגיות). אנרגיה חברותית ונטייה לסטוצים.",
        4: "אדם ביקורתי (כלפי עצמו ואחרים), פרפקציוניסט. חשיבה מסודרת ואנליטית, טוב כשכיר ובלימודים. קשה ונוקשה, מנסה לשלוט בזוגיות.",
        5: "מלך בתקשורת (ציון 90), חשיבה מצוינת ומהירה. נטייה לפרוץ מסגרות, בזבזנות ונהנתנות. קליטה מצוינת לשפות.",
        6: "חשיבה הססנית, שואף לאיזון. עדיף כשכיר. דחף לטפל באחרים, צורך בשיתופיות. טובים בסחיטה רגשית. טוב לזוגיות.",
        7: "מלך בידע וחוכמה (ציון 100), אך רגשית ציון 20. ההתנהלות בזוגיות מהרגש (גורם לטעויות). נטייה למחלות נפש וחוסר איזון.",
        8: "מלך בתכנון וביצוע. חשיבה הישגית, תכליתית ואנליטית. לוקח סיכונים מחושבים. יודע לשלוט במספרים קארמתיים. מצוין בכל תחום.",
        9: "ראייה מרחבית רחבה, חשיבה אנרגטית אנליטית. יכולות חשיבה לשכיר מעולות. חיסרון: קושי בגביית כסף. מצוין בזוגיות.",
        11: "נוטה להתנהל כ-2. נטייה לגמגום או אפילפסיה.",
        13: "חשיבה מפוצלת, ביקורתי ונוקשה (כלפי עצמו וסביבה). מלך ברעיונות לא ישימים. אדם קיצוני בדעותיו. סובל מהפרעות קשב וריכוז מורכבות. לא מתאים לעצמאי.",
        14: "מייצר בעיות בזוגיות. מלא ברעיונות עסקיים (לא ישימים). יכולת ביטוי מצוינת ותקשורתי. נטייה לקחת סיכונים מעבר לקצה.",
        16: "אנרגיה שמייצרת בעיות ודוחה זוגיות. מלך בעצות לאחרים (לא לעצמו) וברעיונות לא ישימים. פריק שליטה, ביקורתי וציני. נטייה לפשיטות רגל כעצמאי.",
        19: "מנסה לשלוט באנשים אחרים. נוטה לקורבנות או מקרבן. חשיבה וביטוי בינוניים.",
        22: "נוטה להתנהל כ-4 (ביקורתי, מסודר).",
        33: "נוטה להתנהל כ-6, אך חזק יותר בהתמדה."
    },
    # הותאם מ'צ'אקרת העין השלישית'
    'תדר התת מודע': { 
        7: "אנרגיה שמייצרת בעיות בזוגיות, חרדות והפסדים כספיים.",
        13: "הופך את האדם לקשה ונוקשה, שהכל צריך להיות אך ורק בדרך שלו.",
        14: "אנרגיה המושכת זוגיות אך מנסה לפרק אותה בכל רגע אפשרי. בנה לעצמו עתיד ללא כסף, זוגיות או מערכות יחסים.",
        16: "האדם בנה לעצמו עתיד עם בעיות בזוגיות, הפסדים כספיים, בעיות נפשיות, חרדות ודיכאונות (מניה דיפרסיה).",
        19: "בחוויה הפנימית עבר אירוע טראומטי. יוצר לעצמו עתיד קורבני, חוסר ביטחון עצמי, בעיות קשב וריכוז ונטייה להתמכרויות.",
        1: "תת מודע טוב שמקדם את האדם.", 
        2: "תת מודע חלש, תלותי, מחפש זוגיות ואישור מהסביבה.",
        3: "תת מודע קליל, מקדם שמחת חיים וחופש.",
        4: "תת מודע יציב, מעדיף מסגרות וסדר.",
        5: "תת מודע תקשורתי, מקדם גבולות ומיניות.",
        6: "תת מודע משפחתי, מקדם נתינה וטיפול באחרים.",
        8: "תת מודע הישגי, דוחף לניהול ולעצמאות.",
        9: "תת מודע רוחני, דוחף להנהגה ולקידום האנושות.",
        11: "תת מודע מאסטר, דוחף לטיפול באחרים ולפיתוח אישי."
    },
    # הותאם מ'צ'אקרת הכתר'
    'תדר התשוקה': { 
        1: "יום לידה חזק: עוזר להתקדם בחיים (במיוחד בשיא 2 ו-3). העולם מזמן הזדמנויות לניהול ולקידום עסקי.",
        2: "יום לידה מעכב: מעכב בתחומים של זוגיות, שיתופי פעולה וקושי בעסקים (לא משפיע לרעה כשכיר).",
        3: "יום לידה מצוין: משיכה לספורט, מוזיקה ואומנות. נטייה להיות עצמאי.",
        4: "יום לידה יציב: היקום מזמן הזדמנויות לרכישת נדל\"ן ונכסים (בשיא 2 ו-3). יום לידה מצוין לשכירים, חלש יחסית לעסקים.",
        5: "יום לידה מצוין: דומה ל-3, עם אנרגיה נוספת של מחשבים, אינטרנט וראיית חשבון. אנשים מיניים עם תקשורת טובה.",
        6: "יום לידה פרווה: לא עוזר ולא מונע. היקום עוזר להקים משפחה.",
        7: "יום לידה מעכב: משפיע לרעה החל מהשיא השני. הכל הולך יותר קשה, מאופיין בהרבה חרדות וקריסות נפשיות. יכול להצליח בספורט.",
        8: "יום לידה מצוין: דוחף לעצמאות וניהול. טריקי: עלול להסתבך עם כספים ורשויות (לעצמאים).",
        9: "יום לידה חזק: מייצר תהפוכות בגיל 2 ו-3. אם האדם יודע להתמודד, התהפוכות יקדמו אותו.",
        11: "יום לידה חזק: נטייה לחרדות וקריסות נפשיות ללא מפה חזקה. דוחף להמצאות רוחניות.",
        13: f"קרמה חונקת. מגיע לשיא בשיא 2 ו-3. מושך לטיפול. {KARMIC_WARNING}",
        14: f"כמו 13: בעיה במסגרות ומערכות יחסים. {KARMIC_WARNING}",
        16: f"כמו 13: קארמה מעכבת רוחנית, משפיע על הנפש. {KARMIC_WARNING}",
        19: f"כמו 13: קארמה מעכבת קורבנית. יש להיזהר שלא להיכנס לכלא בתקופה זו. {KARMIC_WARNING}",
        22: "יום לידה חזק: דוחף קדימה. יש לו את המאסטר החזק ביותר (להמצאות וחידושים). אם נופל, צריך להתרומם לבד.",
        33: "יום לידה חזק: תומך בבניית משפחה יציבה."
    },
    # הותאם מ'צ'אקרת היקום'
    'תדר מזל אסטרולוגי': { 
        1: "מזל אריה (מצוין): דוחף קדימה, כריזמטי, מלך ברעיונות ובביצוע. טוב בתפקידי ניהול.",
        2: "מזל סרטן (מעכב): צריך מפה חזקה כדי להתקדם. אנשים תלותיים, טובים כשכירים, חלשים כעצמאים.",
        3: "מזל קשת (מצוין): דוחף קדימה להיות עצמאי. משיכה לספורט, מוזיקה ואומנות.",
        4: "מזל בתולה (יציב): טוב מאוד במסגרות.",
        5: "מזל תאומים (מצוין): דוחף קדימה, חזק בתקשורת. התמחויות בספורט, מחשבים ואינטרנט.",
        6: "מזל מאזניים (פרווה): טוב לפוליטיקה ולמשפחתיות.",
        7: "מזל דגים (מעכב): מייצר קשיים. 100 בשכל, 20 ברגש (נטייה לפעול מהרגש).",
        8: "מזל גדי (מצוין): דוחף קדימה, אך עלול להפוך אנשים למתוסכלים פנימית אם לא מצליחים לממש את הפוטנציאל הגבוה.",
        9: "מזל טלה (מצוין): דוחף קדימה, מתאים לעצמאים. אימפולסיבי (לא תמיד מסיים).",
        11: "מזל דלי (מעכב): נקרא מזל ספונג'ה, מתקשה להגיע לדרגת מאסטר. חייב מפה חזקה.",
        22: "מזל עקרב (החזק ביותר): דוחף קדימה מאוד חזק. ייעוד גבוה להשאיר חותם, להביא המצאות לעולם. יוצר ביטחון עצמי חזק.",
        33: "מזל שור (טוב): מזל יציב, טוב למשפחה. נטייה לשליטה במערכות יחסים."
    }
}

# 2. פונקציות עזר וצמצום 
# ------------------------------------------------
def reduce_number(n, special_rules=True, reduce_all=False):
    """מצמצם מספר. special_rules=True שומר על מאסטרים וקארמה. reduce_all=True תמיד מצמצם לחד-ספרתי."""
    if reduce_all:
        while n > 9:
            n = sum(int(digit) for digit in str(n))
        return n
    
    while n > 9 and n not in SPECIAL_NUMBERS:
        n = sum(int(digit) for digit in str(n))
    return n

def calculate_name_sum(name_part, letters_map, return_unreduced=False):
    """מחשב סכום גימטרי לחלק נתון של השם."""
    total = 0
    name_part = name_part.replace(" ", "")
    for char in name_part:
        if char in letters_map:
            total += letters_map[char]
    if return_unreduced: return total
    return reduce_number(total, special_rules=True)

# 3. חישוב תאריך לידה 
# ------------------------------------------------
# 🚨 תיקון לוגי בפונקציית המזלות
def get_astro_sign(day, month):
    """מחשב את המזל האסטרולוגי על בסיס יום וחודש ומחזיר את שם המזל."""
    if (month == 3 and day >= 21) or (month == 4 and day <= 19): return 'טלה'
    if (month == 4 and day >= 20) or (month == 5 and day <= 20): return 'שור'
    if (month == 5 and day >= 21) or (month == 6 and day <= 20): return 'תאומים'
    if (month == 6 and day >= 21) or (month == 7 and day <= 22): return 'סרטן'
    if (month == 7 and day >= 23) or (month == 8 and day <= 22): return 'אריה'
    if (month == 8 and day >= 23) or (month == 9 and day <= 22): return 'בתולה'
    if (month == 9 and day >= 23) or (month == 10 and day <= 22): return 'מאזניים'
    if (month == 10 and day >= 23) or (month == 11 and day <= 21): return 'עקרב'
    if (month == 11 and day >= 22) or (month == 12 and day <= 21): return 'קשת'
    if (month == 12 and day >= 22) or (month == 1 and day <= 19): return 'גדי'
    if (month == 1 and day >= 20) or (month == 2 and day <= 18): return 'דלי'
    if (month == 2 and day >= 19) or (month == 3 and day <= 20): return 'דגים'
    return 'לא נמצא' # אם המערכת מגיעה לכאן, יש בעיה בנתוני הקלט

def calculate_birth_data(day, month, year):
    """מחשב את תדרי הלידה הראשיים (תשוקה, ייעוד, אסטרולוגי)."""
    day_reduced = reduce_number(day, special_rules=True)
    
    # צמצום חודשים מיוחד 10->1, 12->3, 11 נשאר 11
    if month == 10:
        month_val = 1
    elif month == 12:
        month_val = 3
    elif month == 11:
        month_val = 11
    else:
        month_val = month

    month_reduced = reduce_number(month_val, special_rules=True)
    year_reduced = reduce_number(year, special_rules=True) # שנה מצומצמת (שומר מאסטר/קארמה)
    year_reduced_single = reduce_number(year, reduce_all=True)
    destiny_number = reduce_number(day_reduced + month_reduced + year_reduced, special_rules=True)
    astro_sign = get_astro_sign(day, month)
    astro_number = ASTRO_MAP.get(astro_sign, None)
    
    return day_reduced, month_val, month_reduced, year_reduced, year_reduced_single, destiny_number, astro_number, astro_sign

# 4. חישוב תדרי שם
# ------------------------------------------------
def calculate_name_freqs(first_name, last_name, destiny_number):
    """מחשב את כל תדרי השם והצ'אקרות הנלוות."""
    all_letters_map = GIMATRIA_MAP 
    
    # חישוב סכומים לא מופחתים
    fn_all_sum_unreduced = calculate_name_sum(first_name, all_letters_map, return_unreduced=True)
    ln_all_sum_unreduced = calculate_name_sum(last_name, all_letters_map, return_unreduced=True)
    consonants_map = {k: v for k, v in all_letters_map.items() if k in CONSONANTS}
    fn_consonants_sum_unreduced = calculate_name_sum(first_name, consonants_map, return_unreduced=True)
    ln_consonants_sum_unreduced = calculate_name_sum(last_name, consonants_map, return_unreduced=True)
    fn_vowels_sum_unreduced = calculate_name_sum(first_name, VOWELS_MAP, return_unreduced=True) 
    ln_vowels_sum_unreduced = calculate_name_sum(last_name, VOWELS_MAP, return_unreduced=True)
    
    # צמצום חלקי
    fn_reduced = reduce_number(fn_all_sum_unreduced, special_rules=True)
    ln_reduced = reduce_number(ln_all_sum_unreduced, special_rules=True)
    fn_consonants_reduced = reduce_number(fn_consonants_sum_unreduced, special_rules=True)
    ln_consonants_reduced = reduce_number(ln_consonants_sum_unreduced, special_rules=True)
    fn_vowels_reduced = reduce_number(fn_vowels_sum_unreduced, special_rules=True)
    ln_vowels_reduced = reduce_number(ln_vowels_sum_unreduced, special_rules=True)
    
    # 1. תדר השם (צ'אקרת העל)
    name_freq_full = fn_reduced
    
    # 2. תדר תעסוקה (צ'אקרת המין והיצירה)
    career_freq = reduce_number(fn_reduced + ln_reduced, special_rules=True) 
    
    # 3. תדר סביבתי (צ'אקרת הבסיס)
    env_freq = reduce_number(fn_consonants_reduced + ln_consonants_reduced, special_rules=True)
    
    # 4. תדר חשיבה וביטוי (צ'אקרת הגרון)
    exp_freq = reduce_number(fn_vowels_reduced + ln_vowels_reduced, special_rules=True)

    # 5. תדר תת מודע (צ'אקרת העין השלישית)
    subconscious_freq = reduce_number(destiny_number + career_freq, special_rules=True)
    
    # 6. תדר חוסר (צ'אקרת הלב)
    destiny_for_lack = reduce_number(destiny_number, reduce_all=True) 
    career_for_lack = reduce_number(career_freq, reduce_all=True) 
    lack_freq = abs(destiny_for_lack - career_for_lack)
    
    return {
        'תדר סביבתי': env_freq, 'תדר תעסוקה': career_freq, 'תדר החוסר': lack_freq,
        'תדר הביטוי והחשיבה': exp_freq, 'תדר התת מודע': subconscious_freq, 'תדר השם': name_freq_full
    }

# 5. חישוב מחזורי חיים (P, W)
# ------------------------------------------------
def calculate_life_cycles(day_reduced, month_val, year_reduced, destiny_number):
    """מחשב את 4 מחזורי החיים (P - אנרגיה ראשית) ואת רצון היקום/אתגרים (W)."""
    
    D = day_reduced
    M_p = reduce_number(month_val, special_rules=True)
    Y_p = year_reduced # שנה מצומצמת (שומר מאסטר/קארמה)

    # ערכים מצומצמים לספרה בודדת (לצורך חישוב האתגרים)
    M_w = reduce_number(month_val, reduce_all=True) 
    D_w = reduce_number(D, reduce_all=True) 
    Y_w = reduce_number(year_reduced, reduce_all=True) 
    
    # אנרגיה ראשית (P)
    p1 = reduce_number(M_p + D, special_rules=True) 
    p2 = reduce_number(D + Y_p, special_rules=True)
    p3 = reduce_number(p1 + p2, special_rules=True)
    p4 = reduce_number(M_p + Y_p, special_rules=True)
    
    # רצון היקום/אתגרים (W) - תמיד חד-ספרתי
    w1_val = abs(M_w - D_w); w1 = reduce_number(w1_val, reduce_all=True)
    w2_val = abs(D_w - Y_w); w2 = reduce_number(w2_val, reduce_all=True)
    w3_val = abs(w1 - w2); w3 = reduce_number(w3_val, reduce_all=True)
    w4_val = abs(M_w - Y_w); w4 = reduce_number(w4_val, reduce_all=True)
    
    # אנרגיה משנית (M - המתנות)
    m1 = M_p 
    m2 = D 
    m3 = D 
    m4 = Y_p 
    
    cycles = {'1': {'משנית': m1, 'ראשית': p1, 'יקום': w1}, 
              '2': {'משנית': m2, 'ראשית': p2, 'יקום': w2}, 
              '3': {'משנית': m3, 'ראשית': p3, 'יקום': w3}, 
              '4': {'משנית': m4, 'ראשית': p4, 'יקום': w4}}
    
    # חישוב תקופות חיים (Periods)
    A = reduce_number(destiny_number, reduce_all=True) 
    end1 = 37 - A
    periods = {
        '1': f"0-{end1}",
        '2': f"{end1}-{end1 + 9}",
        '3': f"{end1 + 9}-{end1 + 18}",
        '4': f"{end1 + 18}-120"
    }
    return cycles, periods

# 6. יצירת טקסט עוצמה ו-DataFrames
# ------------------------------------------------
def get_strength_text(freq_name, freq_value, astro_sign=None):
    """מחזירה את טקסט העוצמה על בסיס ערך התדר."""
    is_master = freq_value in ALL_MASTER_NUMBERS
    is_karmic = freq_value in KARMIC_NUMBERS
    
    def get_key(key):
        return STRENGTH_TEXT_MAP.get(key, '➖ תדר מאוזן')

    if is_karmic: return get_key('KARMIC')
    if is_master: return get_key('MASTER')

    if freq_name in {'אנרגיה ראשית'}:
        if freq_value in {1, 5, 8, 9}: return get_key('STRONG')
        if freq_value in {2, 7}: return get_key('WEAK')
        if freq_value in {3, 4, 6}: return get_key('MEDIUM')

    if freq_name in {'רצון היקום', 'תדר החוסר'}:
        if freq_value == 0: return '⚪ אתגר חזק במיוחד'
        if freq_value in {1, 3, 5, 8, 9}: return get_key('STRONG')
        if freq_value in {2, 4, 6, 7}: return get_key('WEAK')
        
    if freq_name in {'תדר הייעוד', 'תדר התשוקה', 'תדר סביבתי', 'תדר תעסוקה', 'תדר הביטוי והחשיבה', 'תדר התת מודע', 'תדר השם'}:
        if freq_value in {1, 5, 8, 9}: return get_key('STRONG')
        if freq_value in {2, 7}: return get_key('WEAK')
        if freq_value in {3, 4, 6}: return get_key('MEDIUM')

    if freq_name == 'תדר מזל אסטרולוגי':
        if astro_sign in {'עקרב', 'שור'}: return get_key('MASTER')
        if astro_sign in {'טלה', 'אריה', 'גדי', 'תאומים', 'קשת'}: return get_key('STRONG')
        if astro_sign in {'מאזניים', 'בתולה'}: return get_key('MEDIUM')
        if astro_sign in {'סרטן', 'דגים', 'דלי'}: return get_key('WEAK')
        return get_key('NEUTRAL')
        
    return get_key('NEUTRAL')

# 🚨 פונקציה זו תוקנה כדי לקרוא את המפתח הנכון במילון
def get_chakra_description_text(freq_value, chakra_name):
    """מחזירה תיאור מילולי על בסיס תדר הצ'אקרה ושמה החדש."""
    
    description_map = CHAKRA_ANALYSIS.get(chakra_name) 
    
    if description_map and freq_value in description_map:
        return description_map[freq_value]
    
    # טיפול מיוחד בערך 0
    if chakra_name == 'תדר החוסר' and freq_value == 0:
        return CHAKRA_ANALYSIS['תדר החוסר'][0]
    
    # במקרה של מזל אסטרולוגי, אם לא מצא ערך ספציפי (למשל, 33), יחזיר הודעה מפורטת
    if chakra_name == 'תדר מזל אסטרולוגי' and freq_value is not None:
         return f"תדר מזל אסטרולוגי ({freq_value}) לא מוגדר במילון הניתוח המילולי."
    
    return f"לא נמצא ניתוח מילולי מדויק (תדר {freq_value}) עבור {chakra_name}."

# 7. פונקציית הפעלה ראשית
# ----------------------------------------------------

def run_numerology_tool(day, month, year, first_name, last_name):
    """מריץ את כל החישובים ומחזיר את ה-DataFrames לתצוגה ב-Streamlit."""
    
    day_reduced, month_val, month_reduced, year_reduced, year_reduced_single, destiny_number, astro_number, astro_sign = \
        calculate_birth_data(day, month, year)
    
    # 1. מחזורי חיים
    cycles, periods = calculate_life_cycles(day_reduced, month_val, year_reduced, destiny_number)
    cycle_data = []
    
    for cycle, values in cycles.items():
        period = periods[cycle]
        
        # חישוב עוצמות לכל עמודה
        m_strength = get_strength_text('אנרגיה משנית', values['משנית']) 
        p_strength = get_strength_text('אנרגיה ראשית', values['ראשית'])
        w_strength = get_strength_text('רצון היקום', values['יקום'])

        cycle_data.append([
            f"מחזור {cycle}", period, 
            f"{values['משנית']} ({m_strength})", # אנרגיה משנית
            f"{values['ראשית']} ({p_strength})", # אנרגיה ראשית
            f"{values['יקום']} ({w_strength})", # רצון היקום
            values['משנית'], values['ראשית'], values['יקום'] # ערכים נקיים לצביעה
        ])
        
    df_cycles = pd.DataFrame(cycle_data, columns=[
        'מחזור', 'טווח גילאים', 'אנרגיה משנית', 'אנרגיה ראשית', 'רצון היקום', 
        '__משנית_נקי', '__ראשית_נקי', '__יקום_נקי' 
    ])
    
    # 2. תדרי השם ותדרי הלידה
    name_freqs = calculate_name_freqs(first_name, last_name, destiny_number)
    
    # יצירת מפה כללית של כל התדרים עם שמות העמודות החדשים
    freqs_map = {
        'תדר הייעוד (שביל הגורל)': {'freq': destiny_number, 'category': 'לידה'},
        'תדר התשוקה (יום הלידה)': {'freq': day_reduced, 'category': 'לידה'},
        'תדר מזל אסטרולוגי': {'freq': astro_number, 'category': 'לידה', 'sign': astro_sign},
        
        'תדר סביבתי': {'freq': name_freqs['תדר סביבתי'], 'category': 'שם'},
        'תדר תעסוקה': {'freq': name_freqs['תדר תעסוקה'], 'category': 'שם'},
        'תדר החוסר': {'freq': name_freqs['תדר החוסר'], 'category': 'שם'},
        'תדר הביטוי והחשיבה': {'freq': name_freqs['תדר הביטוי והחשיבה'], 'category': 'שם'},
        'תדר התת מודע': {'freq': name_freqs['תדר התת מודע'], 'category': 'שם'},
        'תדר השם': {'freq': name_freqs['תדר השם'], 'category': 'שם'}
    }
    
    birth_data = []
    name_data = []
    analysis_text = []

    for name, info in freqs_map.items():
        freq = info['freq']
        
        # טיפול מיוחד בתדר האסטרולוגי
        if name == 'תדר מזל אסטרולוגי':
            strength = get_strength_text(name, freq, info['sign'])
            value_display = f"{freq} ({info['sign']})"
        else:
            strength = get_strength_text(name, freq)
            value_display = freq

        row = [name, value_display, strength, freq]
        
        # 🚨 יצירת ניתוח מילולי - שימוש בשם התדר הנקי כ-Key
        name_for_analysis = name.split('(')[0].strip()
        desc = get_chakra_description_text(freq, name_for_analysis)
        
        # אם התיאור לא מכיל את הודעת השגיאה "לא נמצא ניתוח" - נציג אותו
        if "לא נמצא ניתוח" not in desc:
            analysis_text.append(f"**{name}** ({freq}): {desc}")

        if info['category'] == 'לידה':
            birth_data.append(row)
        else:
            name_data.append(row)

    df_birth = pd.DataFrame(birth_data, columns=['שם התדר', 'ערך נומרולוגי', 'עוצמת התדר', '__תדר_נקי'])
    df_name = pd.DataFrame(name_data, columns=['שם התדר', 'ערך נומרולוגי', 'עוצמת התדר', '__תדר_נקי'])

    return df_cycles, df_birth, df_name, "\n\n".join(analysis_text)


# -------------------------------------------------------------------------------------------------
# 8. קוד הממשק של Streamlit (לצורך הצגת התוצאות)
# -------------------------------------------------------------------------------------------------

# מפת צבעים סופית
COLOR_MAP_HTML = {
    '⭐ תדר מאסטר': '#DC143C',     # אדום (MASTER)
    '⚠️ תדר חלש/מעכב': '#0000FF',  # כחול (WEAK: 2, 7)
    '❌ תדר קארמתי': '#A9A9A9',    # אפור (KARMIC: 13, 14, 16, 19)
    '✅ תדר חזק': '#FFFF00',       # צהוב (STRONG)
    '➖ תדר מאוזן': '#F0F2F6',     # אפור בהיר (MEDIUM/NEUTRAL)
    '⚪ אתגר חזק במיוחד': '#C0C0C0' # אפור מתכתי
}

def style_cycles_table(df, df_full_data):
    """צובעת את טבלת מחזורי החיים."""
    
    df_style = pd.DataFrame('', index=df.index, columns=df.columns)
    
    p_freq_col = 'אנרגיה ראשית'
    w_freq_col = 'רצון היקום'
    
    for i, row in df_full_data.iterrows():
        p_freq = row['__ראשית_נקי']
        w_freq = row['__יקום_נקי']
        
        p_strength = get_strength_text('אנרגיה ראשית', p_freq)
        w_strength = get_strength_text('רצון היקום', w_freq)

        # צביעת P: מאסטר/קארמה/חזק
        if p_strength == '⭐ תדר מאסטר חזק':
            df_style.loc[i, p_freq_col] = f'background-color: {COLOR_MAP_HTML["⭐ תדר מאסטר"]}; color: white; font-weight: bold;'
        elif p_strength == '❌ תדר קארמתי - היזהר':
            df_style.loc[i, p_freq_col] = f'background-color: {COLOR_MAP_HTML["❌ תדר קארמתי"]}; color: white;'
        elif p_strength == '✅ תדר חזק ומקדם':
            df_style.loc[i, p_freq_col] = f'background-color: {COLOR_MAP_HTML["✅ תדר חזק"]}; color: black;'
            
        # צביעת W: אתגר 0 / חלש
        if w_strength == '⚪ אתגר חזק במיוחד':
            df_style.loc[i, w_freq_col] = f'background-color: {COLOR_MAP_HTML["⚪ אתגר חזק במיוחד"]}; color: black; font-weight: bold;'
        elif w_strength == '⚠️ תדר חלש/מעכב':
            df_style.loc[i, w_freq_col] = f'background-color: {COLOR_MAP_HTML["⚠️ תדר חלש/מעכב"]}; color: white;'
            
    return df_style

def highlight_general_table(s):
    """צובעת שורה בטבלאות הלידה והשם לפי טקסט העוצמה."""
    
    strength_text = s['עוצמת התדר']
    
    style = COLOR_MAP_HTML['➖ תדר מאוזן']
    text_color = 'black'
    
    if '⭐ תדר מאסטר' in strength_text:
        style = COLOR_MAP_HTML['⭐ תדר מאסטר']
        text_color = 'white'
    elif '❌ תדר קארמתי' in strength_text:
        style = COLOR_MAP_HTML['❌ תדר קארמתי']
        text_color = 'white'
    elif '⚠️ תדר חלש/מעכב' in strength_text: 
        style = COLOR_MAP_HTML['⚠️ תדר חלש/מעכב']
        text_color = 'white'
    elif '✅ תדר חזק' in strength_text:
        style = COLOR_MAP_HTML['✅ תדר חזק']
        text_color = 'black'
        
    return [f'background-color: {style}; color: {text_color}; font-weight: bold;'] * len(s)


def main():
    
    st.set_page_config(
        page_title="נומרולוגית התדר - תומר עולם נוי", 
        layout="wide", 
        initial_sidebar_state="expanded"
    )
    
    # CSS מותאם אישית ל-RTL ולמרכוז
    st.markdown("""
        <style>
        /* הגדרת כיוון כללי מימין לשמאל */
        div.stApp { direction: rtl; }
        h1, h2, h3 { text-align: right; }
        
        /* עיצוב כללי לטבלאות - מרכוז וגבולות */
        .stDataFrame table, .stDataFrame th, .stDataFrame td {
            text-align: center !important; 
            vertical-align: middle !important;
            font-size: 1.2em;
            border: 1px solid #333;
            padding: 8px 15px; 
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.title("🔢 נומרולוגית התדר - תומר עולם נוי")
    st.markdown("---")
    
    # 1. קליטת קלט ממשתמש ב-Sidebar 
    with st.sidebar:
        st.header("הזנת נתונים")
        
        st.subheader("תאריך לידה")
        today = datetime.now()
        
        col_d, col_m, col_y = st.columns(3)
        day = col_d.number_input("יום (DD):", min_value=1, max_value=31, value=26, key="d")
        month = col_m.number_input("חודש (MM):", min_value=1, max_value=12, value=11, key="m")
        year = col_y.number_input("שנה (YYYY):", min_value=1900, max_value=today.year, value=1976, key="y")
        
        st.subheader("שם מלא (בעברית)")
        first_name = st.text_input("שם פרטי:", "תומר")
        last_name = st.text_input("שם משפחה:", "נוי")
        
        st.markdown("---")
        
        calculate_button = st.button("לחץ לחישוב וניתוח התדרים", use_container_width=True)

    # 2. הצגת התוצאות
    if calculate_button or st.session_state.get('calculated', False):
        st.session_state['calculated'] = True
        
        try:
            # קריאה לפונקציה המאוחדת
            df_cycles, df_birth, df_name, analysis_text = run_numerology_tool(
                day, month, year, first_name, last_name
            )
            
            # ------------------------------------------------------
            # טבלה 1: מחזורי חיים (Cycle Table)
            # ------------------------------------------------------
            st.header("1. מחזורי החיים")
            
            # עמודות לתצוגה סופית
            cols_to_display = ['מחזור', 'טווח גילאים', 'אנרגיה משנית', 'אנרגיה ראשית', 'רצון היקום']
            df_cycles_display = df_cycles[cols_to_display]
            
            # החלת סגנונות על טבלת המחזורים
            styled_df_cycles = df_cycles_display.style.apply(
                style_cycles_table, df_full_data=df_cycles, axis=None
            )
            
            st.dataframe(styled_df_cycles, use_container_width=True, hide_index=True)
            
            st.markdown("---")

            # ------------------------------------------------------
            # טבלה 2: תדרי הלידה
            # ------------------------------------------------------
            st.header("2. תדרי הלידה")
            
            df_birth_display = df_birth[['שם התדר', 'ערך נומרולוגי', 'עוצמת התדר']]
            styled_df_birth = df_birth_display.style.apply(
                highlight_general_table, axis=1
            )
            st.dataframe(styled_df_birth, use_container_width=True, hide_index=True)

            st.markdown("---")
            
            # ------------------------------------------------------
            # טבלה 3: מפת תדרי השם
            # ------------------------------------------------------
            st.header("3. מפת תדרי השם")
            
            df_name_display = df_name[['שם התדר', 'ערך נומרולוגי', 'עוצמת התדר']]
            styled_df_name = df_name_display.style.apply(
                highlight_general_table, axis=1
            )
            st.dataframe(styled_df_name, use_container_width=True, hide_index=True)

            st.markdown("---")
            
            # ------------------------------------------------------
            # 4. ניתוח השילובים
            # ------------------------------------------------------
            st.header("4. שילובים (ניתוח אישיות)")
            
            if analysis_text:
                st.markdown(analysis_text)
            else:
                st.info("לא נמצאו נתונים לניתוח שילובים.")
            
        except Exception as e:
            st.error(f"אירעה שגיאה בחישוב הנומרולוגי. ודא שהקלט נכון. שגיאה: {e}")

# ----------------------------------------------------
# הפעלת האפליקציה (כנקודת כניסה ראשית)
# ----------------------------------------------------
if __name__ == '__main__':
    main()
