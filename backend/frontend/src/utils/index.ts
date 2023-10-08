function containsDuplicates(array: File[]) {
  const filenames = array.map(
    (x) => x.name.substring(0, x.name.lastIndexOf(".")) || x.name
  );
  if (filenames.length !== new Set(filenames).size) {
    return true;
  }

  return false;
}

const convertFileSize = (fileSize: number) => {
  return fileSize / 1024 > 1024
    ? `${Math.round(fileSize / (1024 * 1024))} MB`
    : `${Math.round(fileSize / 1024)} KB`
};

const getFileExtension = (filename: string) => {
  const extension = filename.substring(
    filename.lastIndexOf(".") + 1,
    filename.length
  );
  return extension;
};

export { containsDuplicates, convertFileSize, getFileExtension };
