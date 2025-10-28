import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

describe('App component', () => {
    it('renders the app title', () => {
        render(<App />);
        const titleElement = screen.getByText(/app title/i);
        expect(titleElement).toBeInTheDocument();
    });

    it('renders a button', () => {
        render(<App />);
        const buttonElement = screen.getByRole('button', { name: /click me/i });
        expect(buttonElement).toBeInTheDocument();
    });
});