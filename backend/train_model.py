import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils import resample
import joblib

print("=" * 50)
print("TRUSTA - Email Model Training")
print("=" * 50)

# ✅ Load dataset
df = pd.read_csv("dataset.csv", sep='\t', names=["label", "message"])
df = df.dropna()
print(f"Total rows loaded: {len(df)}")
print(f"Label distribution:\n{df['label'].value_counts()}\n")

# ✅ Convert labels
df["label"] = df["label"].map({"ham": 0, "spam": 1})
df = df.dropna()

# ✅ Fix imbalance by oversampling spam (minority class)
df_ham = df[df["label"] == 0]
df_spam = df[df["label"] == 1]

df_spam_upsampled = resample(df_spam,
                              replace=True,
                              n_samples=len(df_ham),
                              random_state=42)

df_balanced = pd.concat([df_ham, df_spam_upsampled])
df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

print(f"Balanced dataset size: {len(df_balanced)}")
print(f"Balanced distribution:\n{df_balanced['label'].value_counts()}\n")

X = df_balanced["message"]
y = df_balanced["label"]

# ✅ Better TF-IDF settings
vectorizer = TfidfVectorizer(
    max_features=5000,
    stop_words='english',
    ngram_range=(1, 2),       # use both single words and pairs
    min_df=2,                  # ignore very rare words
    sublinear_tf=True          # apply log normalization
)
X_vec = vectorizer.fit_transform(X)

# ✅ Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y, test_size=0.2, random_state=42, stratify=y
)

# ✅ Train best model - Logistic Regression with tuned settings
print("Training model...")
model = LogisticRegression(
    max_iter=1000,
    C=5,                      # stronger regularization control
    solver='lbfgs',
    class_weight='balanced'   # extra weight to spam class
)
model.fit(X_train, y_train)

# ✅ Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\n" + "=" * 50)
print(f"✅ Accuracy: {accuracy * 100:.2f}%")
print("=" * 50)
print("\nDetailed Report:")
print(classification_report(y_test, y_pred, target_names=["Ham (Safe)", "Spam (Phishing)"]))

# ✅ Save model
joblib.dump(model, "email_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("\n✅ Model saved as email_model.pkl")
print("✅ Vectorizer saved as vectorizer.pkl")