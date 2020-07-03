// Content Script: file that runs in the context of the web page the user is on
console.log("Content Script Running...");
// This is probably where I will be making the context menu functionality
chrome.contextMenus.create({
    title: "Warp Search",
    contexts:["selection"], // ContextType
    onclick: usePythonWarpSearch // do the function that activates your program, (takes in selection, creates tabs
    // the whole shtick
})
