import { render, screen } from '@testing-library/react';
import Home from '../page';

describe('Home Page', () => {
  it('renders the main heading', () => {
    render(<Home />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveTextContent('Roots Revealed');
  });

  it('renders the dashboard link', () => {
    render(<Home />);
    const dashboardLink = screen.getByText(/Go to Dashboard/i);
    expect(dashboardLink).toBeInTheDocument();
    expect(dashboardLink).toHaveAttribute('href', '/dashboard');
  });

  it('renders the Symbolon demo link', () => {
    render(<Home />);
    const symbolonLink = screen.getByText(/Symbolon Demo/i);
    expect(symbolonLink).toBeInTheDocument();
    expect(symbolonLink).toHaveAttribute('href', '/symbolon-demo');
  });
});
