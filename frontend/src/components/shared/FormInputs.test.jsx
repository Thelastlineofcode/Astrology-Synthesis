import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import TextInput from './TextInput';
import Select from './Select';
import Checkbox from './Checkbox';
import Radio, { RadioGroup } from './Radio';

describe('TextInput component', () => {
  it('renders with label', () => {
    render(<TextInput label="Name" value="" onChange={() => {}} />);
    expect(screen.getByLabelText('Name')).toBeInTheDocument();
  });

  it('shows required asterisk when required', () => {
    render(<TextInput label="Email" value="" onChange={() => {}} required />);
    expect(screen.getByLabelText('required')).toBeInTheDocument();
  });

  it('displays error message', () => {
    render(<TextInput label="Email" value="" onChange={() => {}} error="Invalid email" />);
    expect(screen.getByRole('alert')).toHaveTextContent('Invalid email');
  });

  it('displays helper text when no error', () => {
    render(<TextInput label="Name" value="" onChange={() => {}} helperText="Enter your full name" />);
    expect(screen.getByText('Enter your full name')).toBeInTheDocument();
  });

  it('hides helper text when error is shown', () => {
    render(
      <TextInput
        label="Name"
        value=""
        onChange={() => {}}
        helperText="Enter your full name"
        error="Name is required"
      />
    );
    expect(screen.queryByText('Enter your full name')).not.toBeInTheDocument();
    expect(screen.getByText('Name is required')).toBeInTheDocument();
  });

  it('calls onChange when value changes', () => {
    const handleChange = jest.fn();
    render(<TextInput label="Name" value="" onChange={handleChange} />);
    const input = screen.getByLabelText('Name');
    fireEvent.change(input, { target: { value: 'John' } });
    expect(handleChange).toHaveBeenCalled();
  });

  it('is disabled when disabled prop is true', () => {
    render(<TextInput label="Name" value="" onChange={() => {}} disabled />);
    expect(screen.getByLabelText('Name')).toBeDisabled();
  });

  it('has correct aria-invalid attribute', () => {
    const { rerender } = render(<TextInput label="Name" value="" onChange={() => {}} />);
    expect(screen.getByLabelText('Name')).toHaveAttribute('aria-invalid', 'false');
    
    rerender(<TextInput label="Name" value="" onChange={() => {}} error="Error" />);
    expect(screen.getByLabelText('Name')).toHaveAttribute('aria-invalid', 'true');
  });

  it('links error message with aria-describedby', () => {
    render(<TextInput label="Name" value="" onChange={() => {}} error="Error message" />);
    const input = screen.getByLabelText('Name');
    const errorId = input.getAttribute('aria-describedby');
    expect(errorId).toBeTruthy();
    expect(document.getElementById(errorId)).toHaveTextContent('Error message');
  });

  it('links helper text with aria-describedby', () => {
    render(<TextInput label="Name" value="" onChange={() => {}} helperText="Helper text" />);
    const input = screen.getByLabelText('Name');
    const helperId = input.getAttribute('aria-describedby');
    expect(helperId).toBeTruthy();
    expect(document.getElementById(helperId)).toHaveTextContent('Helper text');
  });
});

describe('Select component', () => {
  const options = [
    { value: 'option1', label: 'Option 1' },
    { value: 'option2', label: 'Option 2' },
    { value: 'option3', label: 'Option 3' },
  ];

  it('renders with label', () => {
    render(<Select label="Country" value="" onChange={() => {}} options={options} />);
    expect(screen.getByLabelText('Country')).toBeInTheDocument();
  });

  it('shows required asterisk when required', () => {
    render(<Select label="Country" value="" onChange={() => {}} options={options} required />);
    expect(screen.getByLabelText('required')).toBeInTheDocument();
  });

  it('renders all options', () => {
    render(<Select label="Country" value="" onChange={() => {}} options={options} />);
    expect(screen.getByText('Option 1')).toBeInTheDocument();
    expect(screen.getByText('Option 2')).toBeInTheDocument();
    expect(screen.getByText('Option 3')).toBeInTheDocument();
  });

  it('renders placeholder option', () => {
    render(
      <Select
        label="Country"
        value=""
        onChange={() => {}}
        options={options}
        placeholder="Select a country"
      />
    );
    expect(screen.getByText('Select a country')).toBeInTheDocument();
  });

  it('displays error message', () => {
    render(<Select label="Country" value="" onChange={() => {}} options={options} error="Required field" />);
    expect(screen.getByRole('alert')).toHaveTextContent('Required field');
  });

  it('calls onChange when selection changes', () => {
    const handleChange = jest.fn();
    render(<Select label="Country" value="" onChange={handleChange} options={options} />);
    const select = screen.getByLabelText('Country');
    fireEvent.change(select, { target: { value: 'option2' } });
    expect(handleChange).toHaveBeenCalled();
  });

  it('is disabled when disabled prop is true', () => {
    render(<Select label="Country" value="" onChange={() => {}} options={options} disabled />);
    expect(screen.getByLabelText('Country')).toBeDisabled();
  });

  it('has correct aria-invalid attribute', () => {
    const { rerender } = render(<Select label="Country" value="" onChange={() => {}} options={options} />);
    expect(screen.getByLabelText('Country')).toHaveAttribute('aria-invalid', 'false');
    
    rerender(<Select label="Country" value="" onChange={() => {}} options={options} error="Error" />);
    expect(screen.getByLabelText('Country')).toHaveAttribute('aria-invalid', 'true');
  });
});

describe('Checkbox component', () => {
  it('renders with label', () => {
    render(<Checkbox label="Accept terms" checked={false} onChange={() => {}} />);
    expect(screen.getByLabelText('Accept terms')).toBeInTheDocument();
  });

  it('is checked when checked prop is true', () => {
    render(<Checkbox label="Accept terms" checked={true} onChange={() => {}} />);
    expect(screen.getByLabelText('Accept terms')).toBeChecked();
  });

  it('is not checked when checked prop is false', () => {
    render(<Checkbox label="Accept terms" checked={false} onChange={() => {}} />);
    expect(screen.getByLabelText('Accept terms')).not.toBeChecked();
  });

  it('calls onChange when clicked', () => {
    const handleChange = jest.fn();
    render(<Checkbox label="Accept terms" checked={false} onChange={handleChange} />);
    fireEvent.click(screen.getByLabelText('Accept terms'));
    expect(handleChange).toHaveBeenCalled();
  });

  it('is disabled when disabled prop is true', () => {
    render(<Checkbox label="Accept terms" checked={false} onChange={() => {}} disabled />);
    expect(screen.getByLabelText('Accept terms')).toBeDisabled();
  });

  it('sets indeterminate state', () => {
    render(<Checkbox label="Accept terms" checked={false} onChange={() => {}} indeterminate />);
    const checkbox = screen.getByLabelText('Accept terms');
    expect(checkbox.indeterminate).toBe(true);
  });
});

describe('Radio component', () => {
  it('renders with label', () => {
    render(<Radio label="Option 1" name="test" value="opt1" checked={false} onChange={() => {}} />);
    expect(screen.getByLabelText('Option 1')).toBeInTheDocument();
  });

  it('is checked when checked prop is true', () => {
    render(<Radio label="Option 1" name="test" value="opt1" checked={true} onChange={() => {}} />);
    expect(screen.getByLabelText('Option 1')).toBeChecked();
  });

  it('is not checked when checked prop is false', () => {
    render(<Radio label="Option 1" name="test" value="opt1" checked={false} onChange={() => {}} />);
    expect(screen.getByLabelText('Option 1')).not.toBeChecked();
  });

  it('calls onChange when clicked', () => {
    const handleChange = jest.fn();
    render(<Radio label="Option 1" name="test" value="opt1" checked={false} onChange={handleChange} />);
    fireEvent.click(screen.getByLabelText('Option 1'));
    expect(handleChange).toHaveBeenCalled();
  });

  it('is disabled when disabled prop is true', () => {
    render(<Radio label="Option 1" name="test" value="opt1" checked={false} onChange={() => {}} disabled />);
    expect(screen.getByLabelText('Option 1')).toBeDisabled();
  });
});

describe('RadioGroup component', () => {
  const options = [
    { value: 'opt1', label: 'Option 1' },
    { value: 'opt2', label: 'Option 2' },
    { value: 'opt3', label: 'Option 3' },
  ];

  it('renders with label', () => {
    render(<RadioGroup label="Choose option" name="test" options={options} value="" onChange={() => {}} />);
    expect(screen.getByText('Choose option')).toBeInTheDocument();
  });

  it('shows required asterisk when required', () => {
    render(<RadioGroup label="Choose option" name="test" options={options} value="" onChange={() => {}} required />);
    expect(screen.getByLabelText('required')).toBeInTheDocument();
  });

  it('renders all options', () => {
    render(<RadioGroup label="Choose option" name="test" options={options} value="" onChange={() => {}} />);
    expect(screen.getByLabelText('Option 1')).toBeInTheDocument();
    expect(screen.getByLabelText('Option 2')).toBeInTheDocument();
    expect(screen.getByLabelText('Option 3')).toBeInTheDocument();
  });

  it('displays error message', () => {
    render(
      <RadioGroup
        label="Choose option"
        name="test"
        options={options}
        value=""
        onChange={() => {}}
        error="Selection required"
      />
    );
    expect(screen.getByRole('alert')).toHaveTextContent('Selection required');
  });

  it('checks the correct radio button based on value', () => {
    render(<RadioGroup label="Choose option" name="test" options={options} value="opt2" onChange={() => {}} />);
    expect(screen.getByLabelText('Option 2')).toBeChecked();
    expect(screen.getByLabelText('Option 1')).not.toBeChecked();
    expect(screen.getByLabelText('Option 3')).not.toBeChecked();
  });

  it('calls onChange when a radio button is clicked', () => {
    const handleChange = jest.fn();
    render(<RadioGroup label="Choose option" name="test" options={options} value="" onChange={handleChange} />);
    fireEvent.click(screen.getByLabelText('Option 2'));
    expect(handleChange).toHaveBeenCalled();
  });
});
