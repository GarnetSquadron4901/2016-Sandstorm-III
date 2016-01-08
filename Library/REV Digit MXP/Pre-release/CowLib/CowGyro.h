//==================================================
// Copyright (C) 2015 Team 1538 / The Holy Cows
//==================================================

#ifndef __COW_GYRO_H__
#define __COW_GYRO_H__

//#include <WPIErrors.h>
#include <NetworkCommunication/UsageReporting.h>
#include <AnalogInput.h>
#include <Gyro.h>
#include <Timer.h>
#include "../Declarations.h"
#include "CowCircularBuffer.h"

namespace CowLib
{
	class CowGyro : public SensorBase
	{
	private:
		typedef struct
		{
			int64_t value;
			uint32_t count;
		} st_Accumulation;

		CowCircularBuffer *m_CircularBuffer;
		AnalogInput *m_Analog;
		double m_VoltsPerDegreePerSecond;
		int64_t m_Center;
		double m_Offset;
		double m_LastSaveTime;
		bool m_RecalQueued;
		double TimeSinceLastSave();
		CowGyro();

	public:
		CowGyro(uint32_t channel);
		~CowGyro();
		void SetSensitivity(double voltsPerDegreePerSecond);
		double GetAngle();
		void Reset();
		void HandleCalibration();
		void FinalizeCalibration();
	};
}

#endif
