import { render, screen } from '@testing-library/react';
import Home from '../page';

describe('Home Page', () => {
  it('renders the main heading', () => {
    render(<Home />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeInTheDocument();
  });

  it('renders the Deploy Now link', () => {
    render(<Home />);
    const deployLink = screen.getByText(/Deploy Now/i);
    expect(deployLink).toBeInTheDocument();
  });

  it('renders the Documentation link', () => {
    render(<Home />);
    const docsLink = screen.getByText(/Documentation/i);
    expect(docsLink).toBeInTheDocument();
  });
});
