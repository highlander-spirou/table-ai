import csvImg from "../assets/csv.png";
import xlsxImg from "../assets/xlsx.png";
import { convertFileSize, getFileExtension } from "../utils";

interface UploadedFileProps {
  file: File;
  valid: boolean;
}

const UploadedFile = ({ file, valid }: UploadedFileProps) => {
  let imgSrc = getFileExtension(file.name) === "csv" ? csvImg : xlsxImg;

  return (
    <div className="flex border-2 rounded-xl h-20 w-[275px]">
      <img src={imgSrc} className="ml-5 h-[95%]" />
      <div className="flex flex-col mt-3 ml-5">
        <div className="tooltip text-left" data-tip={`${file.name}`}>
          <p
            className={`${
              valid ? "text-slate-700" : "text-red-500"
            } font-semibold text-base w-[150px] whitespace-nowrap overflow-hidden text-ellipsis`}
          >
            {file.name}
          </p>
        </div>
        <p className="text-sm text-slate-700">{convertFileSize(file.size)}</p>
      </div>
    </div>
  );
};

export default UploadedFile;
