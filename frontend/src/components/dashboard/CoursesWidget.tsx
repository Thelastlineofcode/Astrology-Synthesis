'use client';

import React from 'react';
import WidgetCard from './WidgetCard';

interface CourseItem {
  id: string;
  name: string;
  code: string;
  status: 'Open' | 'Closed' | 'Waitlist' | 'Enrolled';
}

interface CoursesWidgetProps {
  title: string;
  subtitle?: string;
  courses: CourseItem[];
  viewMoreLink?: string;
}

export default function CoursesWidget({ title, subtitle, courses, viewMoreLink }: CoursesWidgetProps) {
  const headerAction = viewMoreLink ? (
    <a href={viewMoreLink} className="text-sm text-[var(--color-primary)] hover:underline flex items-center gap-1">
      ↗️
    </a>
  ) : null;

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Open':
        return 'bg-[var(--color-success)] text-white';
      case 'Closed':
        return 'bg-[var(--color-error)] text-white';
      case 'Waitlist':
        return 'bg-[var(--color-warning)] text-[var(--color-neutral-900)]';
      case 'Enrolled':
        return 'bg-[var(--color-info)] text-white';
      default:
        return 'bg-[var(--color-neutral-200)] text-[var(--text-primary)]';
    }
  };

  return (
    <WidgetCard title={title} headerAction={headerAction}>
      {subtitle && (
        <div className="mb-4 pb-4 border-b border-[var(--border-color)]">
          <p className="text-[var(--text-secondary)]">{subtitle}</p>
        </div>
      )}
      
      {courses.length === 0 ? (
        <p className="text-[var(--text-secondary)] text-center py-8">No courses available</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {courses.map((course) => (
            <div
              key={course.id}
              className="p-4 rounded-lg border border-[var(--border-color)] bg-white dark:bg-[var(--bg-secondary)] hover:shadow-lg transition-shadow"
            >
              <h4 className="font-semibold text-[var(--text-primary)] mb-1">{course.name}</h4>
              <p className="text-sm text-[var(--text-secondary)] mb-3">{course.code}</p>
              <button 
                className={`w-full py-2 px-4 text-sm rounded-lg font-medium transition-colors ${getStatusColor(course.status)}`}
              >
                {course.status}
              </button>
            </div>
          ))}
        </div>
      )}
    </WidgetCard>
  );
}
