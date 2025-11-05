import { render, screen, fireEvent } from "@testing-library/react";
import LoginPage from "../app/auth/login/page";

Object.defineProperty(window, "location", { value: { href: "/" } });

describe("LoginPage", () => {
  test("submits email and password", async () => {
    global.fetch = jest.fn().mockResolvedValue({ ok: true, json: async () => ({ access_token: "t" }) });

    render(<LoginPage />);

    fireEvent.change(screen.getByPlaceholderText(/email/i), { target: { value: "a@b.com" } });
    fireEvent.change(screen.getByPlaceholderText(/password/i), { target: { value: "secret" } });
    fireEvent.click(screen.getByRole("button", { name: /sign in/i }));

    expect(global.fetch).toHaveBeenCalled();
  });
});
