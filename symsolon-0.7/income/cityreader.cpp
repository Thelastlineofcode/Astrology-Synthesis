#include <QFile>

#include <quazip/quazip.h>
#include <quazip/quazipfile.h>

#include <QTextStream>
#include <QList>

/*
class CityReader
{

public:

	CityReader( QString fileName );
	~CityReader();
	
	QList<QString> search( QString searchSearchName );

private:

	QString cityArchiveFileName;

}
*/


int main()
{
  QString		searchName = "budapest";

  QuaZip zip("cities.zip");

  if (!zip.open(QuaZip::mdUnzip))
  {
    qWarning("Couldn't open zip archive: %d", zip.getZipError());
    return -1;
  }

  if (!zip.goToFirstFile())
  {
    qWarning("Couldn't go to first file: %d", zip.getZipError());
    return -1;
  }

  QuaZipFile file(&zip);

  if( !file.open( QIODevice::ReadOnly ) )
  {
    qWarning("Couldn't open file inside zip: %d", file.getZipError());
    return -1;
  }

  QTextStream		text( &file );
  QString		line, cityName;
  quint64		size=0, pos=0, lineNumber=0;
  
  size = file.size();
  
  // 1st line is just header
  line = text.readLine();
  
  while ( !text.atEnd() )
  {
    line = text.readLine();
    if ( line.section(',', 1, 1).startsWith( searchName, Qt::CaseInsensitive ) )
    {
      qDebug( line.toLatin1() );
    }
    if (lineNumber++ % 30000 == 0)
    {
      pos = file.pos();
      qDebug("pos=%i%%", (int)((100*pos)/size));
    }
  }
  
  file.close();

  if( zip.getZipError()!=UNZ_OK )
  {
    qWarning("testPos(): file.close(raw): %d", file.getZipError());
    return false;
  }

  zip.close();

  if(zip.getZipError()!=UNZ_OK)
  {
    qWarning("zip archive close error: %d", zip.getZipError());
    return -1;
  }

  return 0;
}

