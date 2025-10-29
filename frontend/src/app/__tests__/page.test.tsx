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
    const dashboardLink = screen.getByText(/View Dashboard/i);
    expect(dashboardLink).toBeInTheDocument();
    expect(dashboardLink).toHaveAttribute('href', '/dashboard');
  });

  it('renders the description text', () => {
    render(<Home />);
    const description = screen.getByText(/Explore the depths of your birth chart/i);
    expect(description).toBeInTheDocument();
  });
});
