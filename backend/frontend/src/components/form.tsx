import React, { useState, useRef } from "react";
import { Link } from 'react-router-dom'
import { containsDuplicates } from "../utils";
import UploadedFile from "./UploadFile";

interface ValidFiles {
  name: string;
  ext: string;
  size: string;
}

interface invalidFiles {
  name: string;
  ext: string;
}

const Form = () => {
  const [validFiles, setValidFiles] = useState<File[]>([]);
  const [invalidFiles, setInvalidFiles] = useState<File[]>([]);
  const [success, setSuccess] = useState<string | null>(null);
  const [failureMessage, setFailure] = useState<string | null>(null);

  let ref = useRef<HTMLInputElement>(null)



  const handleUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const uploadFiles = Array.from(e.target.files);

      let isDup = containsDuplicates(uploadFiles);
      // setDuplicated(isDup);
      if (isDup === false) {
        uploadFiles.forEach((element) => {
          if (element.size > 5 * 10 ** 8) {
            setInvalidFiles((oldArr) => [...oldArr, element]);
          } else {
            setValidFiles((oldArr) => [...oldArr, element]);
          }
        });
      } else {
        setFailure("Duplicate in filename");
      }
    }
  };

  const reupload = () => {
    setValidFiles([]);
    setInvalidFiles([]);
    setFailure(null);
    setSuccess(null);
    if (ref.current?.value) {
      ref.current.value = ""
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData();
    validFiles.forEach((el) => {
      formData.append("files", el);
    });
    const response = await fetch("api/uploadfiles", {
      method: "post",
      body: formData,
      credentials: "same-origin",
    });
    const data = await response.json();
    if (response.ok) {
      setSuccess(data);
    } else {
      setFailure(data.detail);
    }
  };


  if (success) {
    return (
      <div className="center-flex flex-col mt-5 text-xl font-bold gap-2">
        <div className="center-flex gap-2">
          <span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={2}
              stroke="currentColor"
              className="w-6 h-6 stroke-green-600"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </span>
          <span className="text-green-600">Upload sucessfully</span>
        </div>
        <p className="text-slate-600">
          Navigate to{" "}
          <Link className="link" to="/">
            dashboard
          </Link>{" "}
          to ask AI
        </p>
      </div>
    );
  }

  if (failureMessage) {
    return (
      <>
        <div className="center-flex flex-col mt-5 text-xl font-bold gap-2">
          <div className="center-flex gap-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={2}
              stroke="currentColor"
              className="w-6 h-6 stroke-rose-600"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"
              />
            </svg>
            <span className="text-rose-600">{failureMessage}</span>
          </div>
          <button
            className="link link-warning"
            onClick={reupload}
            type="button"
          >
            Reupload the file
          </button>
        </div>
      </>
    );
  }

  return (
    <form
      encType="multipart/form-data"
      onSubmit={handleSubmit}
      className="mx-auto w-[400px] mt-10 border-2 rounded-2xl py-5"
    >
      {/* Hidden input button */}
      <input
        type="file"
        name="files"
        id="files"
        multiple
        ref={ref}
        accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, text/csv"
        onChange={handleUpload}
        className="hidden"
      />

      {/* Display upload files */}
      {validFiles.length > 0 || invalidFiles.length > 0 ? (
        <>
          <div className="no-scrollbar pt-3 max-h-[170px] flex flex-col items-center gap-2 overflow-y-scroll">
            {invalidFiles.map((x, index) => {
              return (
                <>
                  <UploadedFile key={index} file={x} valid={false} />
                </>
              );
            })}
            {validFiles.map((x, index) => {
              return (
                <>
                  <UploadedFile key={index} file={x} valid={true} />
                </>
              );
            })}
          </div>
          {invalidFiles.length === 0 && (
            // Successfully upload button
            <>
              <div className="center-flex mt-5 gap-5">
                <button className="btn btn-primary" type="submit">
                  Submit
                </button>
                <div className="tooltip text-left" data-tip="Reupload">
                  <button
                    className="btn btn-ghost"
                    onClick={reupload}
                    type="reset"
                  >
                    <svg
                      className="w-6 h-6"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      strokeWidth={1.5}
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M19.5 12c0-1.232-.046-2.453-.138-3.662a4.006 4.006 0 00-3.7-3.7 48.678 48.678 0 00-7.324 0 4.006 4.006 0 00-3.7 3.7c-.017.22-.032.441-.046.662M19.5 12l3-3m-3 3l-3-3m-12 3c0 1.232.046 2.453.138 3.662a4.006 4.006 0 003.7 3.7 48.656 48.656 0 007.324 0 4.006 4.006 0 003.7-3.7c.017-.22.032-.441.046-.662M4.5 12l3 3m-3-3l-3 3"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            </>
          )}
        </>
      ) : (
        // display upload figure
        <>
          <div
            className={`${validFiles.length > 0 || invalidFiles.length > 0
              ? "hidden"
              : "mx-auto flex flex-col justify-center items-center"
              }`}
          >
            <p>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.2"
                stroke="currentColor"
                className="w-12 h-12"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M12 16.5V9.75m0 0l3 3m-3-3l-3 3M6.75 19.5a4.5 4.5 0 01-1.41-8.775 5.25 5.25 0 0110.233-2.33 3 3 0 013.758 3.848A3.752 3.752 0 0118 19.5H6.75z"
                />
              </svg>
            </p>
            <label htmlFor="files" className="btn btn-outline btn-primary mt-3">
              Click to upload
            </label>
          </div>
        </>
      )}
    </form>
  );
};

export type { ValidFiles, invalidFiles };
export default Form;
