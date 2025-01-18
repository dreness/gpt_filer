chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "FOUND_JSON") {
      console.log("[Background] Received JSON fragments from content script.");
  
      // For simplicity, let's just send each fragment array individually.
      // You might combine them, prompt the user for which to send, etc.
      message.payload.forEach(async (fragment, index) => {
        try {
          console.log(`[Background] Sending JSON fragment #${index+1} to Python server...`);
          
          // Example: POST to local Python server listening on port 5000
          // Adjust the URL and endpoint to match your actual server.
          const response = await fetch("http://127.0.0.1:5000/create_files", {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify(fragment)
          });
  
          if (!response.ok) {
            throw new Error(`Server responded with status: ${response.status}`);
          }
  
          const data = await response.json();
          console.log("[Background] Server response:", data);
  
        } catch (err) {
          console.error("[Background] Failed to send JSON to Python server:", err);
        }
      });
    }
  });
  chrome.action.onClicked.addListener((tab) => {
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      files: ["content-script.js"]
    });
  });
  