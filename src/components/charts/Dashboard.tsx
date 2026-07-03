import React, { useMemo } from 'react';
import EChartsReact from 'echarts-for-react';

interface DashboardProps {
  options: Record<string, any>[];
  layout?: 'single' | 'grid';
  gridCols?: number;
  style?: React.CSSProperties;
  className?: string;
}

/**
 * Dashboard: React island wrapper for multiple ECharts.
 * Takes an array of ECharts option objects and renders them in a grid.
 * client:visible — only hydrates when in viewport.
 * Responsive grid layout via Tailwind classes.
 */
export default function Dashboard({
  options,
  layout = 'grid',
  gridCols = 2,
  style,
  className,
}: DashboardProps) {
  const containerStyle = useMemo(
    () => ({
      ...style,
    }),
    [style]
  );

  const gridClass = `grid gap-6 grid-cols-1 ${gridCols > 1 ? `md:grid-cols-${gridCols}` : ''} w-full`;

  if (layout === 'single') {
    return (
      <div className={className} style={containerStyle}>
        {options.map((option, idx) => (
          <div key={idx} className="my-8">
            <EChartsReact
              option={option}
              style={{ width: '100%', height: '400px' }}
              opts={{ renderer: 'svg' }}
              lazyUpdate={true}
            />
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className={`${gridClass} ${className ?? ''}`} style={containerStyle}>
      {options.map((option, idx) => (
        <EChartsReact
          key={idx}
          option={option}
          style={{ width: '100%', height: '300px' }}
          opts={{ renderer: 'svg' }}
          lazyUpdate={true}
        />
      ))}
    </div>
  );
}
