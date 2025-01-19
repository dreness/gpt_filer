(function() {
    console.log("[Content Script] Searching for JSON fragments...");
  
    // A function to do some basic shape-checking of the data
    function isValidCodeObject(obj) {
      return (
        typeof obj.id === "number" &&
        typeof obj.path === "string" &&
        typeof obj.code === "string"
      );
    }
  
    /**
     * Attempt to find code blocks or <pre> elements that contain JSON
     * matching the structure: [{id, path, code}, ...].
     * This example is naive: it looks for <pre> tags and tries to parse them.
     */
    function findJsonFragments() {
      const fragments = [];
      const preTags = document.querySelectorAll("pre");
      preTags.forEach((pre) => {
        try {
            // if pre.outerText begins with "json"...
            if (pre.outerText.startsWith("json")) {
                console.log("pre.outerText", pre.outerText);
                // Try to extract a JSON array from pre.innerText, which will be everything after the first [
                // and before the last ] character.
                const jsonStart = pre.outerText.indexOf("[");
                const jsonEnd = pre.outerText.lastIndexOf("]");
                const json = pre.outerText.substring(jsonStart, jsonEnd + 1);
                //console.log("json", json);
                const parsed = JSON.parse(json);
                if (Array.isArray(parsed) && parsed.every(isValidCodeObject)) {
                    fragments.push(parsed);
                }
                //console.log("pre.outerText.trim()", pre.outerText.trim());
                // const parsed = JSON.parse(pre.outerText.trim().substring(4));
                // if (Array.isArray(parsed) && parsed.every(isValidCodeObject)) {
                //     fragments.push(parsed);
                // }
            }
        } catch (e) {
            //console.log("Error parsing JSON", e);
            // Not valid JSON or doesn't match our structure; ignore
        }
      });
      return fragments;
    }
  
    // Grab all the valid JSON fragments on the page
    const foundFragments = findJsonFragments();
    if (foundFragments.length > 0) {
      //console.log("[Content Script] Found JSON fragments:", foundFragments);
  
      // Send the fragments to the background service worker
      chrome.runtime.sendMessage({ type: "FOUND_JSON", payload: foundFragments });
    }
  })();
  