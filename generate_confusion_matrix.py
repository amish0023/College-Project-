import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay
import numpy as np

# Your actual Logistic Regression confusion matrix
cm = np.array([
    [204, 5, 0],
    [4, 100, 0],
    [0, 2, 5]
])

labels = ["WEAK", "MODERATE", "STRONG"]

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=labels
)

disp.plot(
    values_format="d",
    cmap="Blues"
)

plt.title("Confusion Matrix - Logistic Regression")
plt.xlabel("Predicted Class")
plt.ylabel("Actual Class")

plt.tight_layout()

# Save high-quality image for research paper
plt.savefig(
    "logistic_regression_confusion_matrix.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()