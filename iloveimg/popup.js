document.getElementById("downloadBtn").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  if (!tab.url.includes("iloveimg.com")) {
    alert("This extension only works on iloveimg.com");
    return;
  }

  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      const xpath = '//*[@id="editor"]/div[2]/div/div/div[2]/img';
      const result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
      const img = result.singleNodeValue;

      if (img && img.src) {
        chrome.runtime.sendMessage({ action: "download", url: img.src });
      } else {
        alert("Image not found at specified XPath.");
      }
    }
  });
});
