export const createUser = async (email: string, password: string) => {
  const resp = await fetch("http://localhost:8000/users/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });
  return await resp.json();
};
