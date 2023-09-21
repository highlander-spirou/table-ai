let files = [];
let room_valid = false;

const convertFileSize = (fileSize) => {
    return fileSize / (1024 * 1024) < 0.2
        ? `${Math.round(fileSize / 1024)} KB`
        : `${Math.round(fileSize / (1024 * 1024))} MB`;
};

const getFileExtension = (filename) => {
    const extension = filename.substring(
        filename.lastIndexOf(".") + 1,
        filename.length
    );
    return extension;
};

const debounce = (func, timeout = 1000) => {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => { func.apply(this, args); }, timeout);
    };
}

const handleUpload = (f) => {
    const uploadFiles = Array.from(f);
    uploadFiles.forEach((element) => {
        if (element.size > 5 * 10 ** 8) {
            files = [...files, {
                name: element.name,
                size: "> 500MB",
                ext: getFileExtension(element.name),
                valid: false,
            }]
        } else {
            files = [...files, {
                name: element.name,
                size: convertFileSize(element.size),
                ext: getFileExtension(element.name),
                valid: true,
            }]
        }
    });
};

const renderFiles = (f) => {
    let inner = ""
    f.forEach(file => {
        const el = `
      <div class="flex border-2 rounded-xl h-20 w-[350px]" >
            <img src="/static/imgs/${file.ext === 'csv' ? 'csv' : 'xlsx'}.png" class="ml-5 h-[95%]" />
            <div class="flex flex-col mt-3 ml-5">
                <div class="tooltip text-left" data-tip="${file.name}">
                    <p class="${file.valid ? 'text-slate-700' : 'text-red-500'} font-semibold text-base w-[220px] whitespace-nowrap overflow-hidden text-ellipsis">${file.name}</p>
                </div>
                <p class="text-base ${file.valid ? 'text-slate-700' : 'text-red-500'}">${file.size}</p>
            </div>
        </div>
      `
    inner += el
    })
    document.getElementById('file-list').innerHTML = inner

}

const toggleRoomInput = (f) => {
    if (f.length > 0) {
        document.getElementById('room_name').classList.remove('hidden')
        document.getElementById('upload-label').classList.add('hidden')
    } else {
        document.getElementById('room_name').classList.add('hidden')
        document.getElementById('upload-label').classList.remove('hidden')
    }
}

document.getElementById("files").addEventListener("change", (e) => {
    handleUpload(e.target.files)
    toggleRoomInput(files)
    renderFiles(files)
});

const targetNode = document.getElementById("response");

const config = { childList: true };

const callback = (mutationList, observer) => {
    for (const mutation of mutationList) {
        if (mutation.type === "childList") {
            const innerElement = mutation.target.querySelector('#room-name-response')
            const status = innerElement.getAttribute('status')
            if (status === 'True') {
                document.getElementById('submit').classList.remove('hidden')
            } else {
                document.getElementById('submit').classList.add('hidden')
            }
        }
    }
};

const observer = new MutationObserver(callback);

observer.observe(targetNode, config)