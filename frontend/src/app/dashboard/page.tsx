'use client';

import React from 'react';
import { redirect } from 'next/navigation';

export default function DashboardPage() {
  // Redirect to statistics page as the default dashboard view
  redirect('/dashboard/statistics');
}
