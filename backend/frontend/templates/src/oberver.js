const observerFactory = (targetNode, callback) => {
    const config = { childList: true };
    const observer = new MutationObserver(callback);
    observer.observe(targetNode, config);
}

const observeResponseHandler = (mutationList, observer) => {
    for (const mutation of mutationList) {
        if (mutation.type === "childList") {
            console.log('active')
            const innerElement = mutation.target.querySelector("#response-status");
            const status = innerElement.getAttribute("status");
            if (status === "True") {
                document.getElementById("submit").classList.remove("hidden");
            } else {
                document.getElementById("submit").classList.add("hidden");
            }
        }
    }
};

export {observerFactory, observeResponseHandler}