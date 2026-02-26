import { theme } from '../theme';

export default function ProgressSteps({ total, current, correct = [] }) {
  return (
    <div style={{ display: 'flex', gap: 6, alignItems: 'center', flexWrap: 'wrap' }}>
      {Array.from({ length: total }, (_, i) => {
        const done = i < current;
        const isCorrect = correct[i] === true;
        const isWrong = correct[i] === false;
        let bg = theme.colors.border;
        if (done && isCorrect) bg = theme.colors.success;
        else if (done && isWrong) bg = theme.colors.error;
        else if (done) bg = theme.colors.textMuted;
        const isCurrent = i === current;
        return (
          <div key={i} style={{
            width: isCurrent ? 24 : 16,
            height: 8,
            borderRadius: 4,
            background: isCurrent ? theme.colors.accent : bg,
            transition: 'all 0.3s ease',
          }} />
        );
      })}
    </div>
  );
}
