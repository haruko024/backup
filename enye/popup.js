function copyChar(char, labelId) {
      navigator.clipboard.writeText(char).then(() => {
        const label = document.getElementById(labelId);
        label.classList.add('show');
        setTimeout(() => label.classList.remove('show'), 1800);
      });
    }

    document.getElementById("copy-n").addEventListener("click", () => copyChar("ñ", "label-n"));
    document.getElementById("copy-N").addEventListener("click", () => copyChar("Ñ", "label-N"));