import { createUser } from "../endpoints";
import classes from "./signup.module.css";

export default function SignUpPage() {
  return (
    <div
      className={classes.container}
      onSubmit={async (e) => {
        e.preventDefault();
        const target = e.target as EventTarget & {
          email: { value: string };
          password: { value: string };
        };
        console.log(
          await createUser(target.email.value, target.password.value)
        );
        target.email.value = "";
        target.password.value = "";
      }}
    >
      <form className={classes.signupForm}>
        <h1>Sign Up</h1>
        <label>
          Email
          <input name="email" type="text" />
        </label>
        <label>
          Password
          <input name="password" type="password" />
        </label>
        <button className={classes.signupButton}>Create Account</button>
      </form>
    </div>
  );
}
