import ReactDOM from "react-dom/client";
import App, { collectionLoader } from "./pages/App";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Upload from "./pages/Upload";
import TableName from "./pages/TableName";
import "./index.css";


const router = createBrowserRouter([
    {
        path: "/",
        element: <App />,
        loader: collectionLoader,
    },
    {
        path: "/:tblName",
        element: <TableName />,

    },
    {
        path: '/upload',
        element: <Upload />
    }
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
    <RouterProvider router={router} />
);
