/**
 * DateTimePicker Component
 * Provides a date and time selection UI using react-datepicker
 * Supports both standalone date/time picking and recurring task patterns
 */

'use client'

import React, { useState, useEffect } from 'react'
import DatePicker from 'react-datepicker'
import 'react-datepicker/dist/react-datepicker.css'

export type RecurrencePattern = 'daily' | 'weekly' | 'bi-weekly' | 'monthly' | 'yearly' | null

export interface DateTimePickerProps {
  // Selected date/time value
  value?: Date | null
  // Callback when date/time changes
  onChange: (date: Date | null) => void
  // Minimum selectable date (default: now)
  minDate?: Date
  // Maximum selectable date
  maxDate?: Date
  // Show time picker (default: true)
  showTimeSelect?: boolean
  // Time interval in minutes (default: 15)
  timeIntervals?: number
  // Date format (default: "MMM d, yyyy h:mm aa")
  dateFormat?: string
  // Placeholder text
  placeholder?: string
  // Enable recurrence pattern selector
  enableRecurrence?: boolean
  // Selected recurrence pattern
  recurrencePattern?: RecurrencePattern
  // Callback when recurrence pattern changes
  onRecurrenceChange?: (pattern: RecurrencePattern) => void
  // Custom class name
  className?: string
  // Disabled state
  disabled?: boolean
  // Show inline calendar (no input field)
  inline?: boolean
}

export const DateTimePicker: React.FC<DateTimePickerProps> = ({
  value,
  onChange,
  minDate,
  maxDate,
  showTimeSelect = true,
  timeIntervals = 15,
  dateFormat = 'MMM d, yyyy h:mm aa',
  placeholder = 'Select date and time',
  enableRecurrence = false,
  recurrencePattern = null,
  onRecurrenceChange,
  className = '',
  disabled = false,
  inline = false,
}) => {
  const [selectedDate, setSelectedDate] = useState<Date | null>(value || null)
  const [selectedRecurrence, setSelectedRecurrence] = useState<RecurrencePattern>(recurrencePattern)

  // Sync with external value changes
  useEffect(() => {
    setSelectedDate(value || null)
  }, [value])

  // Sync with external recurrence changes
  useEffect(() => {
    setSelectedRecurrence(recurrencePattern)
  }, [recurrencePattern])

  const handleDateChange = (date: Date | null) => {
    setSelectedDate(date)
    onChange(date)
  }

  const handleRecurrenceChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const pattern = e.target.value === 'none' ? null : (e.target.value as RecurrencePattern)
    setSelectedRecurrence(pattern)
    if (onRecurrenceChange) {
      onRecurrenceChange(pattern)
    }
  }

  const recurrenceOptions = [
    { value: 'none', label: 'Does not repeat' },
    { value: 'daily', label: 'Daily' },
    { value: 'weekly', label: 'Weekly' },
    { value: 'bi-weekly', label: 'Every 2 weeks' },
    { value: 'monthly', label: 'Monthly' },
    { value: 'yearly', label: 'Yearly' },
  ]

  return (
    <div className={`date-time-picker-container ${className}`}>
      <div className="date-picker-wrapper">
        <DatePicker
          selected={selectedDate}
          onChange={handleDateChange}
          minDate={minDate || new Date()}
          maxDate={maxDate}
          showTimeSelect={showTimeSelect}
          timeIntervals={timeIntervals}
          dateFormat={dateFormat}
          placeholderText={placeholder}
          disabled={disabled}
          inline={inline}
          className={`
            w-full px-4 py-2 rounded-lg border border-gray-300
            focus:border-blue-500 focus:ring-2 focus:ring-blue-200
            transition-all duration-200 outline-none
            disabled:bg-gray-100 disabled:cursor-not-allowed
            ${inline ? 'border-0' : ''}
          `}
          calendarClassName="shadow-lg rounded-lg border border-gray-200"
          timeClassName={() =>
            'hover:bg-blue-100 transition-colors duration-150'
          }
          wrapperClassName="w-full"
        />
      </div>

      {enableRecurrence && selectedDate && (
        <div className="recurrence-selector mt-3">
          <label
            htmlFor="recurrence-pattern"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Repeat
          </label>
          <select
            id="recurrence-pattern"
            value={selectedRecurrence || 'none'}
            onChange={handleRecurrenceChange}
            disabled={disabled}
            className="
              w-full px-4 py-2 rounded-lg border border-gray-300
              focus:border-blue-500 focus:ring-2 focus:ring-blue-200
              transition-all duration-200 outline-none
              disabled:bg-gray-100 disabled:cursor-not-allowed
              bg-white
            "
          >
            {recurrenceOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      )}

      <style jsx global>{`
        /* Custom styles for react-datepicker */
        .react-datepicker {
          font-family: inherit;
          border: 1px solid #e5e7eb;
          border-radius: 0.5rem;
          box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }

        .react-datepicker__header {
          background-color: #f9fafb;
          border-bottom: 1px solid #e5e7eb;
          border-radius: 0.5rem 0.5rem 0 0;
          padding-top: 0.5rem;
        }

        .react-datepicker__current-month {
          font-weight: 600;
          color: #1f2937;
        }

        .react-datepicker__day-name {
          color: #6b7280;
          font-weight: 500;
          font-size: 0.875rem;
        }

        .react-datepicker__day {
          color: #374151;
          border-radius: 0.375rem;
          transition: all 0.15s ease;
        }

        .react-datepicker__day:hover {
          background-color: #dbeafe;
          border-radius: 0.375rem;
        }

        .react-datepicker__day--selected,
        .react-datepicker__day--keyboard-selected {
          background-color: #3b82f6;
          color: white;
          font-weight: 600;
          border-radius: 0.375rem;
        }

        .react-datepicker__day--today {
          font-weight: 600;
          color: #3b82f6;
          border: 1px solid #3b82f6;
          border-radius: 0.375rem;
        }

        .react-datepicker__day--disabled {
          color: #d1d5db;
          cursor: not-allowed;
        }

        .react-datepicker__time-container {
          border-left: 1px solid #e5e7eb;
        }

        .react-datepicker__time-list-item {
          transition: background-color 0.15s ease;
        }

        .react-datepicker__time-list-item:hover {
          background-color: #dbeafe !important;
        }

        .react-datepicker__time-list-item--selected {
          background-color: #3b82f6 !important;
          color: white !important;
          font-weight: 600;
        }

        .react-datepicker__triangle {
          display: none;
        }

        .react-datepicker-popper {
          z-index: 9999;
        }

        .react-datepicker__navigation-icon::before {
          border-color: #6b7280;
        }

        .react-datepicker__navigation:hover .react-datepicker__navigation-icon::before {
          border-color: #3b82f6;
        }
      `}</style>
    </div>
  )
}

export default DateTimePicker
