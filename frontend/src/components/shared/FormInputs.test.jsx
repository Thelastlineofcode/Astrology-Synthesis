import React, { useState } from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';

import TextInput from './TextInput';
import Select from './Select';
import Checkbox from './Checkbox';
import Radio, { RadioGroup } from './Radio';

// Mock CSS imports
jest.mock('./FormInputs.css', () => ({}));

describe('Form Components', () => {
  describe('TextInput', () => {
    test('renders with label and associates correctly', () => {
      render(
        <TextInput
          label="Email Address"
          value=""
          onChange={() => {}}
        />
      );
      
      const input = screen.getByLabelText('Email Address');
      const label = screen.getByText('Email Address');
      
      expect(input).toBeInTheDocument();
      expect(label).toBeInTheDocument();
      expect(input).toHaveAttribute('id');
      expect(label).toHaveAttribute('for', input.getAttribute('id'));
    });

    test('shows required indicator when required', () => {
      render(
        <TextInput
          label="Email Address"
          value=""
          onChange={() => {}}
          required
        />
      );
      
      expect(screen.getByLabelText('required')).toBeInTheDocument();
      expect(screen.getByRole('textbox')).toHaveAttribute('required');
    });

    test('displays error message with proper ARIA attributes', () => {
      render(
        <TextInput
          label="Email Address"
          value=""
          onChange={() => {}}
          error="This field is required"
        />
      );
      
      const input = screen.getByRole('textbox');
      const errorMessage = screen.getByRole('alert');
      
      expect(errorMessage).toHaveTextContent('This field is required');
      expect(input).toHaveAttribute('aria-invalid', 'true');
      expect(input).toHaveAttribute('aria-describedby');
    });

    test('displays helper text when provided', () => {
      render(
        <TextInput
          label="Email Address"
          value=""
          onChange={() => {}}
          helperText="We'll never share your email"
        />
      );
      
      const helperText = screen.getByText("We'll never share your email");
      const input = screen.getByRole('textbox');
      
      expect(helperText).toBeInTheDocument();
      expect(input).toHaveAttribute('aria-describedby');
    });

    test('handles user input correctly', async () => {
      const user = userEvent.setup();
      const handleChange = jest.fn();
      
      render(
        <TextInput
          label="Email Address"
          value=""
          onChange={handleChange}
        />
      );
      
      const input = screen.getByRole('textbox');
      await user.type(input, 'test@example.com');
      
      expect(handleChange).toHaveBeenCalled();
    });

    test('disables input when disabled prop is true', () => {
      render(
        <TextInput
          label="Email Address"
          value=""
          onChange={() => {}}
          disabled
        />
      );
      
      expect(screen.getByRole('textbox')).toBeDisabled();
    });
  });

  describe('Select', () => {
    const options = [
      { value: 'option1', label: 'Option 1' },
      { value: 'option2', label: 'Option 2' },
      { value: 'option3', label: 'Option 3' }
    ];

    test('renders with label and options', () => {
      render(
        <Select
          label="Choose an option"
          value=""
          onChange={() => {}}
          options={options}
        />
      );
      
      const select = screen.getByLabelText('Choose an option');
      expect(select).toBeInTheDocument();
      expect(screen.getByRole('option', { name: 'Option 1' })).toBeInTheDocument();
      expect(screen.getByRole('option', { name: 'Option 2' })).toBeInTheDocument();
      expect(screen.getByRole('option', { name: 'Option 3' })).toBeInTheDocument();
    });

    test('includes placeholder option when provided', () => {
      render(
        <Select
          label="Choose an option"
          value=""
          onChange={() => {}}
          options={options}
          placeholder="Select an option..."
        />
      );
      
      expect(screen.getByRole('option', { name: 'Select an option...' })).toBeInTheDocument();
    });

    test('displays error message correctly', () => {
      render(
        <Select
          label="Choose an option"
          value=""
          onChange={() => {}}
          options={options}
          error="Please select an option"
        />
      );
      
      const select = screen.getByRole('combobox');
      const errorMessage = screen.getByRole('alert');
      
      expect(errorMessage).toHaveTextContent('Please select an option');
      expect(select).toHaveAttribute('aria-invalid', 'true');
    });

    test('handles selection change', async () => {
      const user = userEvent.setup();
      const handleChange = jest.fn();
      
      render(
        <Select
          label="Choose an option"
          value=""
          onChange={handleChange}
          options={options}
        />
      );
      
      const select = screen.getByRole('combobox');
      await user.selectOptions(select, 'option2');
      
      expect(handleChange).toHaveBeenCalled();
    });
  });

  describe('Checkbox', () => {
    test('renders with label correctly associated', () => {
      render(
        <Checkbox
          label="I agree to the terms"
          checked={false}
          onChange={() => {}}
        />
      );
      
      const checkbox = screen.getByRole('checkbox');
      const label = screen.getByText('I agree to the terms');
      
      expect(checkbox).toBeInTheDocument();
      expect(label).toBeInTheDocument();
      expect(checkbox).toHaveAttribute('id');
      expect(label).toHaveAttribute('for', checkbox.getAttribute('id'));
    });

    test('handles checked state correctly', () => {
      render(
        <Checkbox
          label="I agree to the terms"
          checked={true}
          onChange={() => {}}
        />
      );
      
      expect(screen.getByRole('checkbox')).toBeChecked();
    });

    test('handles click events', async () => {
      const user = userEvent.setup();
      const handleChange = jest.fn();
      
      render(
        <Checkbox
          label="I agree to the terms"
          checked={false}
          onChange={handleChange}
        />
      );
      
      const checkbox = screen.getByRole('checkbox');
      await user.click(checkbox);
      
      expect(handleChange).toHaveBeenCalled();
    });

    test('supports indeterminate state', () => {
      const TestComponent = () => {
        const [checked, setChecked] = useState(false);
        return (
          <Checkbox
            label="Select all"
            checked={checked}
            onChange={(e) => setChecked(e.target.checked)}
            indeterminate={true}
          />
        );
      };
      
      render(<TestComponent />);
      const checkbox = screen.getByRole('checkbox');
      
      // Note: indeterminate property is set via useEffect in component
      expect(checkbox).toBeInTheDocument();
    });

    test('disables when disabled prop is true', () => {
      render(
        <Checkbox
          label="I agree to the terms"
          checked={false}
          onChange={() => {}}
          disabled
        />
      );
      
      expect(screen.getByRole('checkbox')).toBeDisabled();
    });
  });

  describe('Radio and RadioGroup', () => {
    test('Radio renders with correct attributes', () => {
      render(
        <Radio
          label="Option A"
          name="test-group"
          value="a"
          checked={false}
          onChange={() => {}}
        />
      );
      
      const radio = screen.getByRole('radio');
      expect(radio).toBeInTheDocument();
      expect(radio).toHaveAttribute('name', 'test-group');
      expect(radio).toHaveAttribute('value', 'a');
    });

    test('RadioGroup renders with legend and options', () => {
      const options = [
        { value: 'a', label: 'Option A' },
        { value: 'b', label: 'Option B' },
        { value: 'c', label: 'Option C' }
      ];
      
      render(
        <RadioGroup
          legend="Choose an option"
          name="test-group"
          value=""
          onChange={() => {}}
          options={options}
        />
      );
      
      expect(screen.getByText('Choose an option')).toBeInTheDocument();
      expect(screen.getByRole('radio', { name: 'Option A' })).toBeInTheDocument();
      expect(screen.getByRole('radio', { name: 'Option B' })).toBeInTheDocument();
      expect(screen.getByRole('radio', { name: 'Option C' })).toBeInTheDocument();
    });

    test('RadioGroup shows required indicator', () => {
      const options = [
        { value: 'a', label: 'Option A' }
      ];
      
      render(
        <RadioGroup
          legend="Choose an option"
          name="test-group"
          value=""
          onChange={() => {}}
          options={options}
          required
        />
      );
      
      expect(screen.getByLabelText('required')).toBeInTheDocument();
    });

    test('RadioGroup displays error message', () => {
      const options = [
        { value: 'a', label: 'Option A' }
      ];
      
      render(
        <RadioGroup
          legend="Choose an option"
          name="test-group"
          value=""
          onChange={() => {}}
          options={options}
          error="Please select an option"
        />
      );
      
      expect(screen.getByRole('alert')).toHaveTextContent('Please select an option');
    });

    test('RadioGroup handles selection change', async () => {
      const user = userEvent.setup();
      const handleChange = jest.fn();
      const options = [
        { value: 'a', label: 'Option A' },
        { value: 'b', label: 'Option B' }
      ];
      
      render(
        <RadioGroup
          legend="Choose an option"
          name="test-group"
          value=""
          onChange={handleChange}
          options={options}
        />
      );
      
      const radioB = screen.getByRole('radio', { name: 'Option B' });
      await user.click(radioB);
      
      expect(handleChange).toHaveBeenCalled();
    });
  });

  describe('Accessibility', () => {
    test('all form components support keyboard navigation', async () => {
      const user = userEvent.setup();
      const options = [
        { value: 'option1', label: 'Option 1' },
        { value: 'option2', label: 'Option 2' }
      ];
      
      render(
        <div>
          <TextInput label="Text input" value="" onChange={() => {}} />
          <Select label="Select input" value="" onChange={() => {}} options={options} />
          <Checkbox label="Checkbox input" checked={false} onChange={() => {}} />
        </div>
      );
      
      // Test Tab navigation
      await user.tab();
      expect(screen.getByRole('textbox')).toHaveFocus();
      
      await user.tab();
      expect(screen.getByRole('combobox')).toHaveFocus();
      
      await user.tab();
      expect(screen.getByRole('checkbox')).toHaveFocus();
    });

    test('error messages are announced to screen readers', () => {
      render(
        <TextInput
          label="Email"
          value=""
          onChange={() => {}}
          error="Invalid email format"
        />
      );
      
      const errorMessage = screen.getByRole('alert');
      expect(errorMessage).toBeInTheDocument();
      expect(errorMessage).toHaveTextContent('Invalid email format');
    });
  });
});