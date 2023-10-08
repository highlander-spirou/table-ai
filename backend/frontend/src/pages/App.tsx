import { useLoaderData, NavLink, Await, defer, useAsyncValue } from "react-router-dom";
import { Suspense } from 'react'
import { convertFileSize } from '../utils'
// function getCookie(name) {
//   let cookie = {};
//   document.cookie.split(";").forEach(function (el) {
//     let [k, v] = el.split("=");
//     cookie[k.trim()] = v;
//   });
//   return cookie[name];
// }

export const collectionLoader = async () => {
  const fetcher = fetch("api/").then(res => res.json());

  return defer({
    data: fetcher
  })

}


function RenderAwaitedData() {
  let { consume, response: data } = useAsyncValue() as RouterData["data"];
  return <>
    <p>{convertFileSize(consume)} / 500MB</p>
    <progress className="progress progress-success w-56" value={consume} max={500*(1024*1024)}></progress>
    {data.length > 0 ? (<div className="flex gap-3">
      {data.map((tblName, index) => {
        return <NavLink key={index} to={`${tblName}`} className="link">{tblName}</NavLink>
      })}
    </div>) : (<p className="text-lg font-semibold">
      You have no table in the collection
    </p>)}
  </>
}


interface RouterData {
  data: {
    response: string[]
    consume: number
  }
}

const App = () => {

  const routerData = useLoaderData() as RouterData;

  return (
    <>
      <div className="flex gap-3">
        <NavLink to="/" className="link">Home</NavLink>
        <NavLink to="/upload" className="link">Upload</NavLink>
      </div>
      <Suspense fallback={<p>loading...</p>}>
        <Await resolve={routerData.data}
          errorElement={<p>Error</p>}
        >
          <RenderAwaitedData />
        </Await>
      </Suspense>
    </>
  );
};

export default App;
