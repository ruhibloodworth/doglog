import { useEffect } from "react";

export default function App() {
  useEffect(() => {
    const load = async () => {
      const resp = await fetch("http://localhost:8000");
      console.log(await resp.json());
    };
    load();
  });
  return (
    <>
      <h1>Dog Log</h1>
    </>
  );
}
