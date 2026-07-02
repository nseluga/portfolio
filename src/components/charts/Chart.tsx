import React, { useMemo, useState, useEffect } from 'react';
import EChartsReact from 'echarts-for-react';

interface ChartProps {
  option: Record<string, any>;
  style?: React.CSSProperties;
  className?: string;
}

/**
 * Chart: React island wrapper for ECharts.
 * Takes an ECharts option object and renders interactively.
 * Responsive by default via echarts-for-react.
 * client:visible — only hydrates when in viewport.
 */
export default function Chart({ option, style, className }: ChartProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const chartStyle = useMemo(
    () => ({
      width: '100%',
      height: '400px',
      ...style,
    }),
    [style]
  );

  if (!mounted) {
    return <div className={className} style={chartStyle} />;
  }

  return (
    <div className={className} role="img" aria-label={option.title?.text || 'Chart visualization'}>
      <EChartsReact
        option={option}
        style={chartStyle}
        opts={{ renderer: 'svg' }}
        lazyUpdate={true}
      />
    </div>
  );
}
