'use client';

import React from 'react';
import WidgetCard from './WidgetCard';

interface Contact {
  id: string;
  name: string;
  identifier: string;
  phone?: string;
  email?: string;
  avatar?: string;
}

interface ContactsWidgetProps {
  title: string;
  contacts: Contact[];
  actionLabel?: string;
}

export default function ContactsWidget({ title, contacts, actionLabel = 'Act as a user' }: ContactsWidgetProps) {
  return (
    <WidgetCard title={title}>
      {contacts.length === 0 ? (
        <p className="text-[var(--text-secondary)] text-center py-8">No contacts</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {contacts.map((contact) => (
            <div
              key={contact.id}
              className="p-4 rounded-lg border border-[var(--border-color)] bg-[var(--bg-primary)] hover:shadow-md transition-shadow"
            >
              <div className="flex items-start gap-3 mb-3">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-[var(--color-accent)] to-[var(--color-primary)] flex items-center justify-center text-white font-semibold text-lg">
                  {contact.avatar || contact.name.charAt(0)}
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-[var(--text-primary)]">{contact.name}</h4>
                  <p className="text-sm text-[var(--text-secondary)]">{contact.identifier}</p>
                </div>
              </div>
              
              {(contact.phone || contact.email) && (
                <div className="space-y-2 mb-3">
                  {contact.phone && (
                    <div className="flex items-center gap-2 text-sm">
                      <span className="text-[var(--color-primary)]">📞</span>
                      <a href={`tel:${contact.phone}`} className="text-[var(--color-primary)] hover:underline">
                        {contact.phone}
                      </a>
                    </div>
                  )}
                  {contact.email && (
                    <div className="flex items-center gap-2 text-sm">
                      <span className="text-[var(--color-primary)]">✉️</span>
                      <a href={`mailto:${contact.email}`} className="text-[var(--color-primary)] hover:underline break-all">
                        {contact.email}
                      </a>
                    </div>
                  )}
                </div>
              )}
              
              <button className="w-full py-2 px-4 text-sm border border-[var(--border-color)] rounded-lg hover:bg-[var(--bg-hover)] transition-colors text-[var(--text-primary)]">
                {actionLabel}
              </button>
            </div>
          ))}
        </div>
      )}
    </WidgetCard>
  );
}
