function getVideoId() {
  const url = new URL(window.location.href);
  return url.searchParams.get("v");
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === "GET_VIDEO_ID") {
    sendResponse({ videoId: getVideoId() });
  }
});

