import { observeResponseHandler, observerFactory } from "./src/oberver"
import csvImg from '../assets/csv.png'
import xlsxImg from '../assets/xlsx.png'
let isUpload = false
let validFiles = []
let invalidFiles = []
let duplicated = null

function containsDuplicates(array) {
    if (array.length !== new Set(array).size) {
        return true;
    }

    return false;
}

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

const handleUpload = (files) => {
    isUpload = true
    const uploadFiles = Array.from(files)
    const filenames = uploadFiles.map(x => x.name.substring(0, x.name.lastIndexOf('.')) || x.name)
    if (containsDuplicates(filenames)) {
        duplicated = true
    } else {
        uploadFiles.forEach(element => {
            if (element.size > 5 * 10 ** 8) {
                invalidFiles = [...invalidFiles, { name: element.name }]
            } else {
                validFiles = [
                    ...validFiles,
                    {
                        name: element.name,
                        size: convertFileSize(element.size),
                        ext: getFileExtension(element.name),
                        valid: true,
                    },
                ];
            }
        })
    }
}

const toggleRoomInput = (files) => {
    if (files.length > 0) {
        document.getElementById("room_name").classList.remove("hidden");
        document.getElementById("upload-label").classList.add("hidden");
    } else {
        document.getElementById("room_name").classList.add("hidden");
        document.getElementById("upload-label").classList.remove("hidden");
    }
};

const renderValidFiles = (files) => {
    let inner = "";
    files.forEach((file) => {
        const el = `
      <div class="flex border-2 rounded-xl h-20 w-[350px]" >
            <img src="${file.ext === "csv" ? `${csvImg}` : `${xlsxImg}`}" class="ml-5 h-[95%]" />
            <div class="flex flex-col mt-3 ml-5">
                <div class="tooltip text-left" data-tip="${file.name}">
                    <p class="text-slate-700 font-semibold text-base w-[220px] whitespace-nowrap overflow-hidden text-ellipsis">${file.name
            }</p>
                </div>
                <p class="text-base first-letter:text-slate-700">${file.size}</p>
            </div>
        </div>
      `;
        inner += el;
    });
    document.getElementById("file-list").innerHTML = inner;
};


const renderInvalidFiles = (files) => {
    let inner = "<p class='font-bold text-base text-center text-red-500'>File(s) size > 500MB</p>";
    files.forEach(file => {
        const el = `
    <div class="flex border-2 rounded-xl h-20 w-[350px]" >
        <img src="/static/imgs/${file.ext === "csv" ? "csv" : "xlsx"}.png" class="ml-5 h-[95%]" />
        <div class="mt-3 ml-5">
            <div class="tooltip text-left" data-tip="${file.name}">
                <p class="text-red-500 font-semibold text-base w-[220px] whitespace-nowrap overflow-hidden text-ellipsis">
                    ${file.name}
                </p>
            </div>
        </div>
    </div>
    `
        inner += el
    })
    document.getElementById("error-files").innerHTML = inner;
}

document.getElementById("files").addEventListener("change", (e) => {
    if (isUpload) {
        validFiles = []
        invalidFiles = []
        duplicated = null
    }
    handleUpload(e.target.files);
    if (duplicated) {
        document.getElementById('error-section').innerHTML = `<p class="flex justify-center text-red-500 text-lg font-bold">Duplicate filename</p>`
    } else {
        document.getElementById('error-section').innerHTML = ""
        if (invalidFiles.length > 0) {
            renderInvalidFiles(invalidFiles)
        } else {
            renderValidFiles(validFiles)
            toggleRoomInput(validFiles);
        }
    }
});


const observeResponse = observerFactory(document.getElementById("response"), observeResponseHandler)

