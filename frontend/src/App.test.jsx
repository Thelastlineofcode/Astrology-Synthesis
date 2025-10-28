import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

describe('App component', () => {
    it('renders the app header', () => {
        render(<App />);
        const titleElement = screen.getByText(/Astrology Chart Calculator/i);
        expect(titleElement).toBeInTheDocument();
    });

    it('renders navigation', () => {
        render(<App />);
        const navElement = screen.getByRole('navigation', { name: /main navigation/i });
        expect(navElement).toBeInTheDocument();
    });
});